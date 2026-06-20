from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import QDate
import mysql.connector

import conexion 

# ============================================================================
# VISTA PARA CARGAR/CREAR NUEVOS EMBALAJES
# ============================================================================
# Esta clase define la interfaz para registrar nuevos tipos de embalajes
# en la base de datos. Incluye validación de datos y manejo de errores.
# ============================================================================

class VistaCargarEmbalaje(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de carga de embalajes.
    #
    # Crea los siguientes campos de entrada:
    #   - Tipo de Embalaje (QLineEdit): Nombre/tipo del embalaje (máx 25 caracteres)
    #   - Stock Inicial (QSpinBox): Cantidad inicial (0 a 100000)
    #   - Costo ($) (QDoubleSpinBox): Precio unitario (0 a 999999.99)
    #   - Botón Guardar: Envía los datos a la BD
    #
    # El botón "Guardar en Base de Datos" llama a procesar_formulario() 
    # cuando se hace clic.
    # ________________________________________________________________________
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout() #Crea un layout vertical para organizar los widgets en la interfaz
        self.setLayout(layout) #Establece el layout creado como el layout principal de la ventana
        
        
        label_titulo = QLabel("Registrar Nuevo Embalaje")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(label_titulo)

        layout.addWidget(QLabel("Tipo de Embalaje:")) #Etiqueta para el campo de tipo de embalaje
        self.input_tipo = QLineEdit()
        self.input_tipo.setMaxLength(25)
        layout.addWidget(self.input_tipo)

        layout.addWidget(QLabel("Stock Inicial:"))
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 100000)
        layout.addWidget(self.input_stock)

        layout.addWidget(QLabel("Costo ($):"))
        self.input_costo = QDoubleSpinBox()
        self.input_costo.setRange(0.0, 999999.99)
        layout.addWidget(self.input_costo)

        self.boton_guardar = QPushButton("Guardar en Base de Datos")
        self.boton_guardar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2b78e4; color: white;")
        self.boton_guardar.clicked.connect(self.procesar_formulario)
        
        layout.addWidget(self.boton_guardar)
        layout.addStretch()
        


    # ________________________________________________________________________
    # procesar_formulario()
    # ________________________________________________________________________
    # Valida y procesa los datos ingresados en el formulario de embalaje.
    #
    # Validaciones realizadas:
    #   1. El campo 'Tipo' no debe estar vacío
    #
    # Flujo de ejecución:
    #   1. Obtiene los valores del formulario
    #   2. Valida que el tipo no esté vacío
    #   3. Arma diccionario con los datos
    #   4. Llama a conexion.guardar_embalaje() para guardar en BD
    #   5. Si éxito: muestra mensaje y limpia formulario
    #   6. Si error: muestra mensaje de error específico
    #
    # Excepciones manejadas:
    #   - Error 1062: Tipo de embalaje ya existe (clave única)
    #   - Otros errores MySQL: Se muestran al usuario
    # ________________________________________________________________________
    
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
                QMessageBox.critical(self, "Error", "Ese tipo de embalaje ya existe.") #Clave única violada
            else:
                QMessageBox.critical(self, "Error BD", f"Error inesperado: {error}")

    # ________________________________________________________________________
    # limpiar_campos()
    # ________________________________________________________________________
    # Reinicia todos los campos del formulario a sus valores por defecto.
    #
    # Operaciones:
    #   - Borra el campo de Tipo
    #   - Establece Stock Inicial a 0
    #   - Establece Costo a 0.0
    #
    # Se ejecuta automáticamente después de un guardado exitoso.
    # ________________________________________________________________________
    def limpiar_campos(self):
        self.input_tipo.clear() #Borra el texto del campo de tipo
        self.input_stock.setValue(0) #Establece el valor del stock a 0
        self.input_costo.setValue(0.0)
