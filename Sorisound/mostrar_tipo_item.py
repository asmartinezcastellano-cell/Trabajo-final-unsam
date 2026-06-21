from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
import conexion


#==========================================================================
#MODULO: mostrar_tipo_item.py
#DESCRIPCION: Tabla de visualización de todos los tipos de ítems registrados
#Carga datos de BD y los muestra en QTableWidget con opción de actualizar
#
#FUNCIONALIDADES:
# - Carga lista completa de tipos de ítems al abrir la vista
# - Muestra tipos de ítems en tabla con columna: Nombre
# - Permite actualizar/refrescar la tabla manualmente
# - Ajusta automáticamente el ancho de las columnas
#
#NOTAS:
# - Los datos se cargan directamente desde la BD
# - La tabla es de solo lectura (consulta)
#
#==========================================================================


class VistaMostrarTipoItem(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        # Título
        titulo = QLabel("Tipos de Ítems Registrados")
        titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        # Tabla para mostrar los tipos de ítems
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(1)
        self.tabla.setHorizontalHeaderLabels(["Tipo de Ítem"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        # Botón para actualizar/refrescar la tabla
        self.boton_refrescar = QPushButton("Actualizar Lista")
        self.boton_refrescar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2ca02c; color: white;")
        self.boton_refrescar.clicked.connect(self.cargar_datos_en_tabla)
        layout.addWidget(self.boton_refrescar)
        
        self.setLayout(layout)
        self.cargar_datos_en_tabla()
   
    # Obtiene datos de BD y rellena la tabla
    def cargar_datos_en_tabla(self):
        try:
            registros = conexion.obtener_todos_los_tipos_item()
            self.tabla.setRowCount(len(registros))
            
            for numero_fila, fila_datos in enumerate(registros):
                item = QTableWidgetItem(str(fila_datos[0]))
                self.tabla.setItem(numero_fila, 0, item)
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {error}")