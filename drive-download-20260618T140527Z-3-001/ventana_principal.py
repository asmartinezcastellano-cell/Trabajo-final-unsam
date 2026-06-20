"""
MÓDULO: ventana_principal.py
DESCRIPCIÓN: Ventana principal de la aplicación SoriSound (GUI)
Gestiona la navegación entre pantallas usando QStackedWidget
Crea el menú principal con opciones CRUD para:
- Embalajes, Tipos de Ítems, Ítems, Procesos, Productos
"""

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
import cargar_proceso
import actualizar_proceso
import mostrar_proceso
import eliminar_proceso
import cargar_producto
import actualizar_producto
import mostrar_producto
import eliminar_producto


# Ventana principal: crea interfaz con menú y contenedor de pantallas
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()# Configura título y tamaño de la ventana
        self.setWindowTitle("Sistema SoriSound")
        self.resize(800,600)

        # QStackedWidget: contiene todas las pantallas (se muestra una a la vez)
        self.contenedor_pantallas = QStackedWidget()# Centraliza el contenedor de pantallas en la ventana principal
        self.setCentralWidget(self.contenedor_pantallas)# Agrega cada pantalla al contenedor (índices fijos para navegación por menú)

        # ==================== EMBALAJES (índices 0-3) ====================
        self.pantalla_crear_embalaje = cargar_embalaje.VistaCargarEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_crear_embalaje)# Agrega pantalla de carga de embalaje al contenedor

        self.pantalla_mostrar_embalaje= mostrar_embalaje.VistaVerEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_embalaje)

        self.pantalla_actualizar_embalaje = actualizar_embalaje.VistaActualizarEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_embalaje)

        self.pantalla_eliminar_embalaje = eliminar_embalaje.VistaEliminarEmbalaje()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_embalaje)

        # ==================== TIPOS DE ITEM (índices 4-6) ====================
        self.pantalla_actualizar_tipo_item = cargar_tipo_item.VistaCargarTipoItem()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_tipo_item)

        self.pantalla_mostrar_tipo_item = mostrar_tipo_item.VistaMostrarTipoItem()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_tipo_item)

        self.pantalla_eliminar_tipo_item = eliminar_tipo_item.VistaEliminarTipoItem()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_tipo_item)

        # ==================== ITEMS (índices 7-10) ====================
        self.pantalla_crear_item = cargar_item.VistaCargarItem()
        self.contenedor_pantallas.addWidget(self.pantalla_crear_item)

        self.pantalla_actualizar_item = actualizar_item.VistaModificarItem()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_item)
        self.pantalla_actualizar_item.refrescar_selectores()# Refresca los combo box de la pantalla de actualización de item para mostrar los últimos datos

        self.pantalla_mostrar_items = mostrar_items.VistaVerItems()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_items)
        self.pantalla_mostrar_items.cargar_datos_tabla()

        self.pantalla_eliminar_item = eliminar_item.VistaEliminarItem()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_item)

        # ==================== PROCESOS (índices 11-14) ====================
        self.pantalla_cargar_proceso = cargar_proceso.VistaCargarProceso()
        self.contenedor_pantallas.addWidget(self.pantalla_cargar_proceso)

        self.pantalla_actualizar_proceso = actualizar_proceso.VistaActualizarProceso()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_proceso)

        self.pantalla_mostrar_proceso = mostrar_proceso.VistaMostrarProcesos()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_proceso)
        
        self.pantalla_eliminar_proceso = eliminar_proceso.VistaEliminarProceso()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_proceso)

        # ==================== PRODUCTOS (índices 15-18) ====================
        self.pantalla_cargar_producto = cargar_producto.VistaCargarProducto() 
        self.contenedor_pantallas.addWidget(self.pantalla_cargar_producto)

        self.pantalla_actualizar_producto = actualizar_producto.VistaModificarProducto()
        self.contenedor_pantallas.addWidget(self.pantalla_actualizar_producto)

        self.pantalla_mostrar_producto = mostrar_producto.VistaListarProductos()
        self.contenedor_pantallas.addWidget(self.pantalla_mostrar_producto)

        self.pantalla_eliminar_producto = eliminar_producto.VistaEliminarProducto()
        self.contenedor_pantallas.addWidget(self.pantalla_eliminar_producto)

        self.crear_menu()# Crea el menú principal con opciones de navegación entre pantallas

    # Crea menú principal con opciones de navegación
    def crear_menu(self):
        barra_menu =self.menuBar()

        menu_archivo = barra_menu.addMenu("&Archivo")
        accion_salir = QAction("Salir",self)
        accion_salir.triggered.connect(self.close)
        menu_archivo.addAction(accion_salir)

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

        menu_proceso = barra_menu.addMenu("&Proceso")

        accion_cargar_proceso = QAction("Cargar un Proceso",self)
        accion_cargar_proceso.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(11))
        menu_proceso.addAction(accion_cargar_proceso)

        accion_actualizar_proceso = QAction("Actualizar Proceso",self)
        accion_actualizar_proceso.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(12))
        menu_proceso.addAction(accion_actualizar_proceso)

        accion_mostrar_proceso = QAction("Mostrar los Procesos",self)
        accion_mostrar_proceso.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(13))
        menu_proceso.addAction(accion_mostrar_proceso)

        accion_eliminar_proceso = QAction("Eliminar un Proceso",self)
        accion_eliminar_proceso.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(14))
        menu_proceso.addAction(accion_eliminar_proceso)

        menu_producto = barra_menu.addMenu("&Producto")


        accion_cargar_producto = QAction("Cargar un Producto",self)
        accion_cargar_producto.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(15))
        menu_producto.addAction(accion_cargar_producto)

        accion_actualizar_producto = QAction("Actualizar un Producto",self)
        accion_actualizar_producto.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(16))
        menu_producto.addAction(accion_actualizar_producto)

        accion_mostrar_producto = QAction("Mostrar un Producto",self)
        accion_mostrar_producto.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(17))
        menu_producto.addAction(accion_mostrar_producto)

        accion_eliminar_producto = QAction("Eliminar un Producto",self)
        accion_eliminar_producto.triggered.connect(lambda:self.contenedor_pantallas.setCurrentIndex(18))
        menu_producto.addAction(accion_eliminar_producto)

# Punto de entrada de la aplicación

if __name__ == "__main__":
    app = QApplication(sys.argv) # Crea la aplicación Qt
    ventana = VentanaPrincipal() # Crea la ventana principal
    ventana.show()  # Muestra la ventana principal
    sys.exit(app.exec()) # Ejecuta el loop de eventos de la aplicación


