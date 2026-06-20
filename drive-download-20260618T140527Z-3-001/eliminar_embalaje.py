# eliminar_embalaje.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QMessageBox)
import mysql.connector
import conexion 

class VistaEliminarEmbalaje(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        label_titulo = QLabel("Eliminar Embalaje")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px; color: #cc0000;")
        layout.addWidget(label_titulo)

        layout.addWidget(QLabel("Seleccione el Tipo de Embalaje a eliminar:"))
        
        self.combo_embalajes = QComboBox()
        layout.addWidget(self.combo_embalajes)

        self.boton_eliminar = QPushButton("Eliminar de la Base de Datos")
        self.boton_eliminar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #d9534f; color: white;")
        self.boton_eliminar.clicked.connect(self.confirmar_eliminacion)
        layout.addWidget(self.boton_eliminar)
        
        layout.addStretch()
        self.setLayout(layout)

    def cargar_combo_box(self):
        self.combo_embalajes.clear()
        
        try:
            
            embalajes = conexion.obtener_todos_los_embalajes() 
            
            if not embalajes:
                self.combo_embalajes.addItem("No hay embalajes registrados")
                self.boton_eliminar.setEnabled(False)
                return
                
            self.boton_eliminar.setEnabled(True)
            for embalaje in embalajes:
                tipo_emb = embalaje[0]
                self.combo_embalajes.addItem(tipo_emb)
                
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los embalajes: {error}")

    def confirmar_eliminacion(self):
        tipo_a_eliminar = self.combo_embalajes.currentText()
        
        if not tipo_a_eliminar or tipo_a_eliminar == "No hay embalajes registrados":
            return

        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación", 
            f"¿Estás seguro de eliminar el embalaje:\n'{tipo_a_eliminar}'?",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            try:
                conexion.eliminar_embalaje(tipo_a_eliminar)
                
                QMessageBox.information(self, "Éxito", "El registro ha sido eliminado correctamente.")
                self.cargar_combo_box() # Refrescar la lista
                
            except mysql.connector.Error as error:
                
                if error.errno == 1451:
                    QMessageBox.critical(
                        self, 
                        "Error de integridad", 
                        f"No se puede eliminar '{tipo_a_eliminar}' porque está asociado a uno o más productos."
                    )
                else:
                    QMessageBox.critical(self, "Error BD", f"No se pudo eliminar: {error}")