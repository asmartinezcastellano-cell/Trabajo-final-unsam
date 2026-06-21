from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QDoubleSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import QDate
import conexion


#==========================================================================
#MODULO: actualizar_proceso.py
#DESCRIPCION: Formulario para actualizar el precio de un proceso registrado en la BD
#Carga datos actuales al seleccionar un proceso, permite modificar y guarda cambios
#
#FUNCIONALIDADES:
# - Carga lista de procesos disponibles en combo box al abrir la vista
# - Al seleccionar un proceso, muestra su precio actual
# - Permite modificar el precio del proceso
# - Valida que el valor sea numérico y positivo
# - Muestra mensajes de confirmación y error según corresponda
#
#NOTAS:
# - Los cambios se guardan inmediatamente en la BD
# - El precio debe ser positivo
#
#===========================================================================

class VistaActualizarProceso(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()# Crea un layout vertical para organizar los widgets
        
        # 1. Título de la ventana
        titulo = QLabel("Actualizar Precio de un Proceso")
        titulo.setStyleSheet("font-size : 20px ; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        # 2. ComboBox para seleccionar el proceso
        layout.addWidget(QLabel("Seleccione el Proceso a modificar:"))
        self.combo_proceso = QComboBox()
        self.combo_proceso.currentIndexChanged.connect(self.cargar_datos_actuales)
        layout.addWidget(self.combo_proceso)     
            
        # 3. Input para el nuevo costo
        layout.addWidget(QLabel("Nuevo Precio / Costo ($):"))
        self.input_costo = QDoubleSpinBox()
        self.input_costo.setRange(0.0, 999999.99)
        self.input_costo.setDecimals(2)
        layout.addWidget(self.input_costo)
        
        # 4. Botón para guardar
        self.boton_actualizar = QPushButton("Guardar Cambios")
        self.boton_actualizar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #ff9800; color: white;")
        self.boton_actualizar.clicked.connect(self.procesar_actualizacion)
        layout.addWidget(self.boton_actualizar)
        
        layout.addStretch()
        self.setLayout(layout)
        
        # Bandera para evitar que el evento currentIndexChanged se dispare al limpiar/cargar el combo
        self.bloquear_senal = False 
        
        # Cargamos los datos iniciales al crear la vista
        self.cargar_combo_box()
        
    def cargar_combo_box(self):
        """Busca todos los tipos de procesos en la BD y los mete en el ComboBox"""
        try:
            self.bloquear_senal = True 
            self.combo_proceso.clear()
            
            # Llamada al nuevo método de conexión
            registros = conexion.obtener_todos_los_tipos_proceso() 
            
            if registros:
                for fila in registros:
                    self.combo_proceso.addItem(fila[0]) # fila[0] es 'tipo_proceso'
                self.bloquear_senal = False
                
                # Fuerza la carga del costo del primer elemento seleccionado
                self.cargar_datos_actuales()
            else:
                self.combo_proceso.addItem("No hay procesos registrados")
                self.bloquear_senal = False
                
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los procesos: {error}")

    def cargar_datos_actuales(self):
        """Va a la base de datos y lee el costo actual del proceso seleccionado"""
        if self.bloquear_senal:
            return
            
        tipo_seleccionado = self.combo_proceso.currentText()
        
        if not tipo_seleccionado or tipo_seleccionado == "No hay procesos registrados":
            return
            
        try:
            # Llamada al método que busca por tipo_proceso
            datos = conexion.obtener_proceso_por_tipo(tipo_seleccionado)
            if datos:
                # 'datos' devuelve una tupla de un solo elemento (costo,)
                costo_actual = datos[0]
                self.input_costo.setValue(float(costo_actual))
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Error al recuperar datos: {error}")

    def procesar_actualizacion(self):
        """Toma el nuevo costo del formulario y ejecuta el UPDATE en la BD"""
        tipo_seleccionado = self.combo_proceso.currentText()
        
        if not tipo_seleccionado or tipo_seleccionado == "No hay procesos registrados":
            QMessageBox.warning(self, "Atención", "No hay un proceso válido seleccionado.")
            return
            
        datos_actualizados = {
            "tipo_proceso": tipo_seleccionado,    
            "costo": self.input_costo.value(),
            "fecha": QDate.currentDate().toString("yyyy-MM-dd") 
        }
        
        try:
            # Llamada al método de actualización
            conexion.actualizar_proceso(datos_actualizados)
            QMessageBox.information(self, "Éxito", f"Proceso '{tipo_seleccionado}' actualizado correctamente.")
        except Exception as error:
            QMessageBox.critical(self, "Error al actualizar", f"No se guardaron los cambios: {error}")