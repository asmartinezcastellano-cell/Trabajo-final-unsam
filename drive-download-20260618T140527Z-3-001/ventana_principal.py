import sys
from PySide6.QtWidgets import (QApplication,QMainWindow, QStackedWidget)
from PySide6.QtGui import QAction
import cargar_embalaje
import mostrar_embalaje
import actualizar_embalaje
import cargar_tipo_item
import mostrar_tipo_item
import eliminar_embalaje
import eliminar_tipo_item
import cargar_item
import actualizar_item
import mostrar_items
import eliminar_item



# ============================================================================
# VENTANA PRINCIPAL DEL SISTEMA SORISOUND
# ============================================================================
# Esta clase define la ventana principal de la aplicación, que actúa como
# contenedor principal para todas las pantallas de gestión de embalajes e items.
# ============================================================================

class VentanaPrincipal(QMainWindow):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la ventana principal y configura todas las pantallas disponibles.
    # 
    # Responsabilidades:
    #   - Crear el contenedor de pantallas (QStackedWidget)
    #   - Instanciar todas las vistas para embalajes, tipos de items e items
    #   - Agregar cada vista al contenedor con un índice específico
    #   - Crear el menú de navegación
    #
    # Pantallas disponibles (índices):
    #   0 - Crear Embalaje
    #   1 - Ver Embalajes
    #   2 - Actualizar Embalaje
    #   3 - Eliminar Embalaje
    #   4 - Crear Tipo Item
    #   5 - Ver Tipos Item
    #   6 - Eliminar Tipo Item
    #   7 - Crear Item
    #   8 - Actualizar Item
    #   9 - Ver Items
    #   10 - Eliminar Item
    # ________________________________________________________________________
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema SoriSound")
        self.resize(800,600)
        
        # Contenedor de pantallas (QStackedWidget) para mostrar una pantalla a la vez.
        self.contenedor_pantallas = QStackedWidget()
        self.setCentralWidget(self.contenedor_pantallas)

        self.pantalla_crear_embalaje = cargar_embalaje.VistaCargarEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_crear_embalaje) #indice 0

        self.pantalla_mostrar_embalaje= mostrar_embalaje.VistaVerEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_embalaje) #indice 1

        self.pantalla_actualizar_embalaje = actualizar_embalaje.VistaActualizarEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_embalaje) #indice 2

        self.pantalla_eliminar_embalaje = eliminar_embalaje.VistaEliminarEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_embalaje) #indice 3

        self.pantalla_actualizar_tipo_item = cargar_tipo_item.VistaCargarTipoItem()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_tipo_item) #indice 4

        self.pantalla_mostrar_tipo_item = mostrar_tipo_item.VistaMostrarTipoItem()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_tipo_item) #indice 5

        self.pantalla_eliminar_tipo_item = eliminar_tipo_item.VistaEliminarTipoItem()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_tipo_item)  #indice 6

        self.pantalla_crear_item = cargar_item.VistaCargarItem()
        self.contenedor_pantallas.addWidget(self.pantalla_crear_item) #indice 7

        self.pantalla_actualizar_item = actualizar_item.VistaModificarItem()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_item) #indice 8
        self.pantalla_actualizar_item.refrescar_selectores()

        self.pantalla_mostrar_items = mostrar_items.VistaVerItems()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_items) #indice 9
        self.pantalla_mostrar_items.cargar_datos_tabla()

        self.pantalla_eliminar_item = eliminar_item.VistaEliminarItem()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_item) #indice 10

        self.crear_menu()

    # ________________________________________________________________________
    # crear_menu()
    # ________________________________________________________________________
    # Construye la barra de menú de la aplicación con todas las opciones de
    # navegación agrupadas por categoría (Archivo, Embalaje, Tipo Item, Item).
    #
    # Estructura del menú:
    #   • Archivo
    #     - Salir: Cierra la aplicación
    #   
    #   • Embalaje
    #     - Cargar Embalaje (índice 0)
    #     - Mostrar Embalajes (índice 1)
    #     - Actualizar Embalaje (índice 2)
    #     - Eliminar Embalaje (índice 3)
    #
    #   • Tipo Item
    #     - Cargar Tipo Item (índice 4)
    #     - Mostrar Tipos Item (índice 5)
    #     - Eliminar Tipo Item (índice 6)
    #
    #   • Item
    #     - Cargar Item (índice 7)
    #     - Actualizar Item (índice 8)
    #     - Mostrar Items (índice 9)
    #     - Eliminar Item (índice 10)
    #
    # Cada opción del menú conecta un lambda que cambia el índice del 
    # QStackedWidget para mostrar la pantalla correspondiente.
    # ________________________________________________________________________
    # Método para crear el menú de la aplicación
    def crear_menu(self):
        barra_menu =self.menuBar()
        

        # Menú Archivo
        menu_archivo = barra_menu.addMenu("&Archivo")
        accion_salir = QAction("Salir",self)
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)
        

        # Menú Embalaje
        menu_embalaje = barra_menu.addMenu("&Embalaje")

        accion_cargar_embalaje = QAction("Cargar Embalaje",self)
        accion_cargar_embalaje.triggered.connect(lambda : self.contenedor_pantallas.setCurrentIndex(0))
        menu_embalaje.addAction(accion_cargar_embalaje)
        
        accion_mostrar_embalaje = QAction("Mostrar Embalajes",self)
        accion_mostrar_embalaje.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(1))
        menu_embalaje.addAction(accion_mostrar_embalaje)

        accion_actualizar_embalaje = QAction("Actualizar Embalaje",self)
        accion_actualizar_embalaje.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(2))
        self.pantalla_actualizar_embalaje.cargar_combo_box()
        menu_embalaje.addAction(accion_actualizar_embalaje)


        accion_eliminar_embalaje = QAction("Eliminar Embalaje",self)
        accion_eliminar_embalaje.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(3))
        self.pantalla_eliminar_embalaje.cargar_combo_box()
        menu_embalaje.addAction(accion_eliminar_embalaje)

        # Menú Tipo Item
        menu_tipo_item = barra_menu.addMenu("&Tipo Item")

        accion_cargar_nuevo_tipo_item= QAction("Cargar Tipo Item",self)
        accion_cargar_nuevo_tipo_item.triggered.connect(lambda : self.contenedor_pantallas.setCurrentIndex(4))
        menu_tipo_item.addAction(accion_cargar_nuevo_tipo_item)

        accion_mostrar_tipo_item = QAction("Mostrar Tipo Item",self)
        accion_mostrar_tipo_item.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(5))
        self.pantalla_mostrar_tipo_item.cargar_datos_en_tabla()
        menu_tipo_item.addAction(accion_mostrar_tipo_item)

        accion_eliminar_tipo_item = QAction("Eliminar Tipo Item",self)
        accion_eliminar_tipo_item.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(6))        
        self.pantalla_eliminar_tipo_item.cargar_combo_box()
        menu_tipo_item.addAction(accion_eliminar_tipo_item) 
        
        # Menú Item
        menu_item = barra_menu.addMenu("&Item")

        accion_cargar_item = QAction("Cargar un Item",self)
        accion_cargar_item.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(7))
        menu_item.addAction(accion_cargar_item)

        accion_actualizar_item = QAction("Actualizar Item",self)
        accion_actualizar_item.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(8))
        menu_item.addAction(accion_actualizar_item)

        accion_mostrar_items = QAction("Mostar Datos Items",self)
        accion_mostrar_items.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(9))
        menu_item.addAction(accion_mostrar_items)

        accion_eliminar_item = QAction("Eliminar Item",self)
        accion_eliminar_item.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(10))
        menu_item.addAction(accion_eliminar_item)
        




# Punto de entrada de la aplicación



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())


