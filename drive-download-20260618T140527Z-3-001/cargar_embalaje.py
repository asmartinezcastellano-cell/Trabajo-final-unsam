"""
MÓDULO: cargar_embalaje.py
DESCRIPCIÓN: Formulario para registrar nuevos embalajes en la BD
Validación de campos, manejo de errores y feedback de usuario
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import QDate
import mysql.connector

import conexion 

# Vista para cargar/registrar nuevo embalaje
class VistaCargarEmbalaje(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        label_titulo = QLabel("Registrar Nuevo Embalaje")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(label_titulo)

        # Campo: tipo de embalaje
        layout.addWidget(QLabel("Tipo de Embalaje:"))
        self.input_tipo = QLineEdit()
        self.input_tipo.setMaxLength(25)
        layout.addWidget(self.input_tipo)

        # Campo: stock inicial
        layout.addWidget(QLabel("Stock Inicial:"))
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 100000)
        layout.addWidget(self.input_stock)

        # Campo: costo
        layout.addWidget(QLabel("Costo ($):"))
        self.input_costo = QDoubleSpinBox()
        self.input_costo.setRange(0.0, 999999.99)
        layout.addWidget(self.input_costo)

        # Botón: guardar en BD
        self.boton_guardar = QPushButton("Guardar en Base de Datos")
        self.boton_guardar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2b78e4; color: white;")
        self.boton_guardar.clicked.connect(self.procesar_formulario)
        
        layout.addWidget(self.boton_guardar)
        layout.addStretch()
        

    # Valida y envía datos al formulario
    def procesar_formulario(self):
        
        tipo_embalaje = self.input_tipo.text().strip()
        
        if not tipo_embalaje:
            QMessageBox.warning(self, "Error de validación", "El campo 'Tipo' es obligatorio.")
            return

       
        datos_embalaje = {
            "tipo": tipo_embalaje,
            "stock": self.input_stock.value(),
            "costo": self.input_costo.value(),
            "fecha": QDate.currentDate().toString("yyyy-MM-dd")
        }

        
        try:
            conexion.guardar_embalaje(datos_embalaje)
            
            
            QMessageBox.information(self, "Éxito", f"Embalaje '{datos_embalaje['tipo']}' registrado.")
            self.limpiar_campos()
            
        except mysql.connector.Error as error:
            
            if error.errno == 1062:
                QMessageBox.critical(self, "Error", "Ese tipo de embalaje ya existe.")
            else:
                QMessageBox.critical(self, "Error BD", f"Error inesperado: {error}")

    # Limpia todos los campos del formulario
    def limpiar_campos(self):
        self.input_tipo.clear()
        self.input_stock.setValue(0)
        self.input_costo.setValue(0.0)
