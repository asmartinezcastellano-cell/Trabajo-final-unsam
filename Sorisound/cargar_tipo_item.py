from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import conexion

class VistaCargarTipoItem(QWidget):
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