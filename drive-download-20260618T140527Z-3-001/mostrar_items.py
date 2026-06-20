from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QAbstractItemView, QHeaderView, QMessageBox)
import conexion

class VistaVerItems(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
    
        layout_superior = QHBoxLayout()
        label_titulo = QLabel("Lista de Ítems / Productos Registrados")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout_superior.addWidget(label_titulo)
        
        #actualiza el contenido de la tabla
        self.boton_refrescar = QPushButton("🔄 Actualizar Tabla")
        self.boton_refrescar.setStyleSheet("padding: 6px 12px; font-weight: bold;")
        self.boton_refrescar.clicked.connect(self.cargar_datos_tabla)
        layout_superior.addWidget(self.boton_refrescar)
        
        layout.addLayout(layout_superior)
        
       
        self.tabla = QTableWidget()
        
       
        columnas = [
            "Código", "Color", "Descripción", "Peso (kg)", "Tipo Item", 
            "Ancho", "Largo", "Diámetro", "Espesor", "Largo Tira", "Precio MP ($)"
        ]
        self.tabla.setColumnCount(len(columnas))
        self.tabla.setHorizontalHeaderLabels(columnas)
        
        # no permite editar el contenido de la tabla 
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows)  
        
        #hace que se estiren los títulos
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tabla.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) 
        layout.addWidget(self.tabla)
        
        # carga los datos a la tabla
        self.cargar_datos_tabla()

    def cargar_datos_tabla(self):
        """Busca los datos en la BD y los dibuja en la tabla"""
        try:
            #limpia las filas
            self.tabla.setRowCount(0)
            
            # trae la lista de items. Cada fila es una tupla
            items = conexion.obtener_todos_los_items_completo()
            
           #llenado de la tabla
            for fila_idx, item in enumerate(items):
                self.tabla.insertRow(fila_idx) 

                for col_idx, valor in enumerate(item):
                    texto_celda = str(valor) if valor is not None else ""                   
                    celda = QTableWidgetItem(texto_celda)                    
                    self.tabla.setItem(fila_idx, col_idx, celda)
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {e}")