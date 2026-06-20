from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, 
                             QMessageBox, QAbstractItemView, QHeaderView)
from PySide6.QtCore import Qt
import conexion

class VistaMostrarProcesos(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        
        cabecera_layout = QHBoxLayout()
        
        titulo = QLabel("Listado de Procesos")
        titulo.setStyleSheet("font-size : 20px ; font-weight:bold;")
        cabecera_layout.addWidget(titulo)
        
        cabecera_layout.addStretch() 
        
        self.boton_refrescar = QPushButton("Actualizar Tabla")
        self.boton_refrescar.setStyleSheet("padding: 6px 12px; font-weight: bold; background-color: #2196F3; color: white;")
        self.boton_refrescar.clicked.connect(self.cargar_datos_en_tabla)
        cabecera_layout.addWidget(self.boton_refrescar)
        
        layout.addLayout(cabecera_layout)
        
       
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Tipo de Proceso", "Costo ($)", "Fecha de Actualización"])
        
       
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        self.tabla.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.tabla.setSelectionMode(QAbstractItemView.SingleSelection) 
        
        
        header = self.tabla.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch) 
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) 
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) 
        
        layout.addWidget(self.tabla)
        self.setLayout(layout)
        
        
        self.cargar_datos_en_tabla()
        
    def cargar_datos_en_tabla(self):
        """Busca los procesos en la base de datos y rellena las celdas"""
        try:
            
            self.tabla.setRowCount(0)
            
            
            registros = conexion.obtener_todos_los_procesos_completo()
            
            if not registros:
                QMessageBox.information(self, "Aviso", "No hay procesos registrados para mostrar.")
                return
                
            
            self.tabla.setRowCount(len(registros))
            
            for num_fila, fila_datos in enumerate(registros):
                # fila_datos contiene: (tipo_proceso, costo, fecha)
                tipo = str(fila_datos[0])
                costo = f"$ {float(fila_datos[1]):,.2f}" 
                fecha = str(fila_datos[2])
                
                
                item_tipo = QTableWidgetItem(tipo)
                item_costo = QTableWidgetItem(costo)
                item_fecha = QTableWidgetItem(fecha)
                
                
                item_costo.setTextAlignment(Qt.AlignCenter)
                item_fecha.setTextAlignment(Qt.AlignCenter)
                
                
                self.tabla.setItem(num_fila, 0, item_tipo)
                self.tabla.setItem(num_fila, 1, item_costo)
                self.tabla.setItem(num_fila, 2, item_fecha)
                
        except Exception as error:
            QMessageBox.critical(self, "Error de Carga", f"No se pudieron cargar los datos de la BD: {error}")