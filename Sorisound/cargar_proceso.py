from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import QDate
import mysql.connector

import conexion 

#==========================================================================
#MODULO: cargar_proceso.py
#DESCRIPCION: Formulario para registrar nuevos procesos en la BD
#Validación de campos, manejo de errores y feedback de usuario
#
#FUNCIONALIDADES:
# - Formulario para ingresar datos de un nuevo proceso (nombre, precio)
# - Valida que los campos no estén vacíos y tengan valores válidos
# - Verifica que el nombre del proceso sea único en la BD
# - Guarda el nuevo proceso en la BD
# - Muestra mensajes de confirmación y error según corresponda
#
#NOTAS:
# - No se permite registrar procesos con el mismo nombre
# - El precio debe ser numérico y positivo
#
#==========================================================================


class VistaCargarProceso(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Título
        label_titulo = QLabel("Registrar Nuevo Proceso")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(label_titulo)
        # Campo: tipo de proceso
        layout.addWidget(QLabel("Tipo de Proceso:"))
        self.input_tipo_proceso = QLineEdit()
        self.input_tipo_proceso.setMaxLength(25)
        layout.addWidget(self.input_tipo_proceso)
        # Campo: costo
        layout.addWidget(QLabel("Costo ($):"))
        self.input_costo_proceso= QDoubleSpinBox()
        self.input_costo_proceso.setRange(0.0, 999999.99)
        layout.addWidget(self.input_costo_proceso)
        # Botón: guardar en BD
        self.boton_guardar = QPushButton("Guardar en Base de Datos")
        self.boton_guardar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2b78e4; color: white;")
        self.boton_guardar.clicked.connect(self.procesar_formulario)
        # Agrega el botón al layout
        layout.addWidget(self.boton_guardar)
        layout.addStretch()
        
    # Valida y envía datos al formulario
    def procesar_formulario(self):
        
        tipo_proceso = self.input_tipo_proceso.text().strip()
        
        if not tipo_proceso:
            QMessageBox.warning(self, "Error de validación", "El campo 'Tipo de Proceso' es obligatorio.")
            return

       
        datos_proceso = {
            "tipo_proceso": tipo_proceso,
            "costo": self.input_costo_proceso.value(),
            "fecha": QDate.currentDate().toString("yyyy-MM-dd")
        }

        # Intenta guardar el proceso en la base de datos y maneja posibles errores
        try:
            conexion.guardar_proceso(datos_proceso)
            
            
            QMessageBox.information(self, "Éxito", f"Proceso '{datos_proceso['tipo_proceso']}' registrado.")
            self.limpiar_campos()
            
        except mysql.connector.Error as error:
            
            if error.errno == 1062:
                QMessageBox.critical(self, "Error", "Ese tipo de proceso ya existe.")
            else:
                QMessageBox.critical(self, "Error BD", f"Error inesperado: {error}")

    def limpiar_campos(self):
        self.input_tipo_proceso.clear()
        self.input_costo_proceso.setValue(0.0)
