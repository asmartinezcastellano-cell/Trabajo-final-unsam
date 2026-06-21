from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView)
import conexion

#==========================================================================
#MODULO: mostrar_embalaje.py
#DESCRIPCION: Tabla de visualización de todos los embalajes registrados
#Carga datos de BD y los muestra en QTableWidget con opción de actualizar
#
#FUNCIONALIDADES:
# - Carga lista completa de embalajes al abrir la vista
# - Muestra embalajes en tabla con columnas: Tipo, Stock, Precio
# - Permite actualizar/refrescar la tabla manualmente
# - Ajusta automáticamente el ancho de las columnas
#
#NOTAS:
# - Los datos se cargan directamente desde la BD
# - La tabla es de solo lectura (consulta)
#
#==========================================================================
class VistaVerEmbalaje(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()        
      
        # Título
        titulo = QLabel("Inventario de Embalajes")
        titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
       
        self.tabla = QTableWidget()
        
        # Configura columnas de la tabla
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Tipo de Embalaje", "Stock", "Costo ($)", "Última Actualización"])
        
        # Estira columnas para ocupar ancho de ventana
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabla)
        
        # Botón: actualizar/refrescar la tabla
        self.boton_refrescar = QPushButton("Actualizar Tabla")
        self.boton_refrescar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2ca02c; color: white;")
        self.boton_refrescar.clicked.connect(self.cargar_datos_en_tabla)
        layout.addWidget(self.boton_refrescar)
        
        self.setLayout(layout)
        
        # Carga datos al inicializar
        self.cargar_datos_en_tabla()

    # Obtiene datos de BD y rellena la tabla
    def cargar_datos_en_tabla(self):
        try:
            # Traigo los datos de BD
            registros = conexion.obtener_todos_los_embalajes()
            
            # Cuenta las filas
            self.tabla.setRowCount(len(registros))
            
            # Llena la tabla celda por celda
            for numero_fila, fila_datos in enumerate(registros):
                for numero_columna, valor in enumerate(fila_datos):
                    item = QTableWidgetItem(str(valor))
                    self.tabla.setItem(numero_fila, numero_columna, item)
                    
        except Exception as error:
            QMessageBox.critical(self, "Error al cargar datos", f"No se pudo leer la base de datos: {error}")