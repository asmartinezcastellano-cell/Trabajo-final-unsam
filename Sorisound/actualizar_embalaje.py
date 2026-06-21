from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import QDate
import conexion

#==========================================================================
#MODULO: actualizar_embalaje.py
#DESCRIPCION: Formulario para actualizar stock y precio de embalajes registrados en la BD
#Carga datos actuales al seleccionar un embalaje, permite modificar y guarda cambios
#
#FUNCIONALIDADES:
# - Carga lista de embalajes disponibles en combo box al abrir la vista
# - Al seleccionar un embalaje, muestra datos actuales (stock y precio)
# - Permite modificar los valores de stock y precio
# - Valida campos antes de guardar cambios en BD
# - Muestra mensajes de confirmación y error según corresponda
#
#NOTAS:
# - Los cambios se guardan inmediatamente en la BD
# - Se valida que los valores sean numéricos y positivos
#
#==========================================================================


class VistaActualizarEmbalaje(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
       
        titulo = QLabel("Actualizar Stock y Precio de Embalaje")
        titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
      
        layout.addWidget(QLabel("Seleccione el Embalaje a modificar:"))
        self.combo_embalajes = QComboBox()
       
        self.combo_embalajes.currentIndexChanged.connect(self.cargar_datos_actuales)
        layout.addWidget(self.combo_embalajes)
        
       
        layout.addWidget(QLabel("Nueva Cantidad / Stock:"))
        self.input_stock = QSpinBox()
        self.input_stock.setRange(0, 100000)
        layout.addWidget(self.input_stock)
        
     
        layout.addWidget(QLabel("Nuevo Precio / Costo ($):"))
        self.input_costo = QDoubleSpinBox()
        self.input_costo.setRange(0.0, 999999.99)
        self.input_costo.setDecimals(2)
        layout.addWidget(self.input_costo)
        

        self.boton_actualizar = QPushButton("Guardar Cambios")
        self.boton_actualizar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #ff9800; color: white;")
        self.boton_actualizar.clicked.connect(self.procesar_actualizacion)
        layout.addWidget(self.boton_actualizar)
        
        layout.addStretch()
        self.setLayout(layout)
        
        
        self.bloquear_señal = False 
        
    def cargar_combo_box(self):
        """Busca todos los tipos de embalaje en la BD y los mete en el ComboBox"""
        try:
            self.bloquear_señal = True 
            self.combo_embalajes.clear()
            
            
            registros = conexion.obtener_todos_los_embalajes() 
            
            if registros:
                for fila in registros:
                    self.combo_embalajes.addItem(fila[0]) # fila[0] es el 'tipo' (nombre)
                self.bloquear_señal = False
                
                self.cargar_datos_actuales()
            else:
                self.combo_embalajes.addItem("No hay embalajes registrados")
                self.bloquear_señal = False
                
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los embalajes: {error}")

    def cargar_datos_actuales(self):
        """Va a la base de datos y lee el stock/costo del embalaje seleccionado"""
        if self.bloquear_señal:
            return
            
        tipo_seleccionado = self.combo_embalajes.currentText()
        
        if not tipo_seleccionado or tipo_seleccionado == "No hay embalajes registrados":
            return
            
        try:
            datos = conexion.obtener_embalaje_por_tipo(tipo_seleccionado)
            if datos:
                stock_actual, costo_actual = datos
                self.input_stock.setValue(stock_actual)
                self.input_costo.setValue(float(costo_actual))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Error al recuperar datos: {error}")

    def procesar_actualizacion(self):
        tipo_seleccionado = self.combo_embalajes.currentText()
        
        if not tipo_seleccionado or tipo_seleccionado == "No hay embalajes registrados":
            QMessageBox.warning(self, "Atención", "No hay un embalaje válido seleccionado.")
            return
            
        
        datos_actualizados = {
            "tipo": tipo_seleccionado,
            "stock": self.input_stock.value(),
            "costo": self.input_costo.value(),
            "fecha": QDate.currentDate().toString("yyyy-MM-dd") 
        }
        
        try:
            conexion.actualizar_embalaje(datos_actualizados)
            QMessageBox.information(self, "Éxito", f"Embalaje '{tipo_seleccionado}' actualizado correctamente.")
        except Exception as error:
            QMessageBox.critical(self, "Error al actualizar", f"No se guardaron los cambios: {error}")