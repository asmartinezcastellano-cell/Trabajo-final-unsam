from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QSpinBox, QDoubleSpinBox, QPushButton, QMessageBox)
from PySide6.QtCore import QDate
import conexion

# ============================================================================
# VISTA PARA ACTUALIZAR EMBALAJES EXISTENTES
# ============================================================================
# Esta clase permite modificar el stock y precio de embalajes ya registrados.
# Incluye validación y actualización de datos en la BD.
# ============================================================================

class VistaActualizarEmbalaje(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de actualización de embalajes.
    #
    # Componentes:
    #   - ComboBox: Seleccionar el embalaje a modificar
    #   - QSpinBox: Nueva cantidad/stock (0 a 100000)
    #   - QDoubleSpinBox: Nuevo precio/costo (0 a 999999.99)
    #   - Botón "Guardar Cambios": Envía los cambios a la BD
    #
    # Variable de control:
    #   - self.bloquear_señal: Previene actualizaciones recursivas al cambiar 
    #     el combo box (evita ciclos infinitos)
    # ________________________________________________________________________
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
        
    # ________________________________________________________________________
    # cargar_combo_box()
    # ________________________________________________________________________
    # Carga todos los embalajes disponibles en el ComboBox para selección.
    #
    # Flujo de ejecución:
    #   1. Bloquea señales para evitar disparos de eventos
    #   2. Limpia el ComboBox actual
    #   3. Obtiene todos los embalajes de BD
    #   4. Agrega cada embalaje al ComboBox (usando el 'tipo' como texto)
    #   5. Desbloquea señales y carga los datos del primer embalaje
    #
    # Casos especiales:
    #   - Si no hay embalajes: muestra "No hay embalajes registrados"
    #
    # Se llama automáticamente cuando se navega a esta pantalla.
    # ________________________________________________________________________
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

    # ________________________________________________________________________
    # cargar_datos_actuales()
    # ________________________________________________________________________
    # Obtiene y muestra los datos actuales (stock y costo) del embalaje 
    # seleccionado en el ComboBox.
    #
    # Flujo de ejecución:
    #   1. Verifica si se debe procesar (bloquear_señal)
    #   2. Obtiene el tipo de embalaje seleccionado
    #   3. Consulta BD para obtener stock y costo actuales
    #   4. Llena los campos de entrada con los valores obtenidos
    #
    # Se ejecuta automáticamente cuando cambia la selección del ComboBox.
    # ________________________________________________________________________
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

    # ________________________________________________________________________
    # procesar_actualizacion()
    # ________________________________________________________________________
    # Valida y envía los cambios de stock y costo a la base de datos.
    #
    # Validaciones:
    #   1. Verifica que haya un embalaje válido seleccionado
    #
    # Flujo de ejecución:
    #   1. Obtiene el embalaje seleccionado
    #   2. Valida que sea un embalaje real
    #   3. Arma diccionario con los nuevos valores
    #   4. Obtiene fecha actual en formato yyyy-MM-dd
    #   5. Envía cambios a BD mediante conexion.actualizar_embalaje()
    #   6. Muestra mensaje de éxito o error
    # ________________________________________________________________________
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