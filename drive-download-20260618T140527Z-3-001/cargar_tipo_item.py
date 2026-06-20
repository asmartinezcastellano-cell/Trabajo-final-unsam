from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import conexion

# ============================================================================
# VISTA PARA CREAR NUEVAS CATEGORÍAS DE TIPOS DE ITEMS
# ============================================================================
# Esta clase define la interfaz para registrar nuevas categor\u00edas de items
# en la base de datos.
# ============================================================================

class VistaCargarTipoItem(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de carga de tipos de items.
    #
    # Componentes:
    #   - Título: "Registrar Nuevo Tipo de Ítem"
    #   - Campo de entrada: Nombre del tipo de item (QLineEdit)
    #   - Botón: "Guardar Tipo de Ítem" que ejecuta procesar_guardado()
    # ________________________________________________________________________
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        titulo = QLabel("Registrar Nuevo Tipo de Ítem")
        titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        layout.addWidget(QLabel("Nombre del Tipo de Ítem :"))
        self.input_nombre = QLineEdit()
        layout.addWidget(self.input_nombre)
        
        self.boton_guardar = QPushButton("Guardar Tipo de Ítem")
        self.boton_guardar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2b78e4; color: white;")
        self.boton_guardar.clicked.connect(self.procesar_guardado)
        layout.addWidget(self.boton_guardar)
        
        layout.addStretch()
        self.setLayout(layout)
        
        
    # ________________________________________________________________________
    # procesar_guardado()
    # ________________________________________________________________________
    # Valida y procesa el nombre del tipo de item ingresado.
    #
    # Validaciones:
    #   1. El campo no debe estar vac\u00edo
    #
    # Flujo de ejecuci\u00f3n:
    #   1. Obtiene y limpia el texto ingresado
    #   2. Valida que no sea vac\u00edo
    #   3. Llama a conexion.guardar_tipo_item() para guardar en BD
    #   4. Si \u00e9xito: muestra mensaje y limpia el campo
    #   5. Si error: muestra mensaje de error
    # ________________________________________________________________________
    def procesar_guardado(self):
        nombre = self.input_nombre.text().strip()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "El campo no puede estar vacío.")
            return
            
        try:
            conexion.guardar_tipo_item(nombre)
            QMessageBox.information(self, "Éxito", f"Tipo '{nombre}' guardado correctamente.")
            self.input_nombre.clear()
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {error}")