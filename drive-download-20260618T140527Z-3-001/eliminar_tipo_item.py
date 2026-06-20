from PySide6.QtWidgets import (QWidget, QVBoxLayout,QLabel,QComboBox,
                               QPushButton, QMessageBox)
import mysql.connector
import conexion

class VistaEliminarTipoItem(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label_titulo = QLabel("Eliminar Tipo de Ítem ")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px; color: #cc0000;")
        layout.addWidget(label_titulo)

        layout.addWidget(QLabel("Seleccione el tipo de ítem que va a eliminar"))

        self.combo_tipo_item = QComboBox()
        layout.addWidget(self.combo_tipo_item)

        self.boton_eliminar = QPushButton("Eliminar de la Base de Datos el Tipo de Item")
        self.boton_eliminar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #d9534f; color: white;")
        self.boton_eliminar.clicked.connect(self.confirmar_eliminacion)
        layout.addWidget(self.boton_eliminar)
        
        layout.addStretch()
        self.setLayout(layout)

    def cargar_combo_box(self):
        self.combo_tipo_item.clear()
        try:
            tipos = conexion.obtener_todos_los_tipos_item()
            if not tipos:
                self.combo_tipo_item.addItem("No hay item disponible")
                self.boton_eliminar.setEnabled(False)
                return
            self.boton_eliminar.setEnabled(True)
            for tipo in tipos:
                tipo_item = tipo[0]
                self.combo_tipo_item.addItem(tipo_item)
        except Exception as error:
            QMessageBox.critical(self, "Error",f"No se pudieron cargar los tipos de items :{error}")


    def confirmar_eliminacion(self):
        tipo_a_eliminar = self.combo_tipo_item.currentText()

        if not tipo_a_eliminar or tipo_a_eliminar == "No hay item disponible":
            return
        
        respuesta = QMessageBox.question(
            self,
            "Confirmar eliminacion",
            f"¿Estás seguro de eliminar el tipo de item\n{tipo_a_eliminar}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            try:
                conexion.borrar_tipo_item(tipo_a_eliminar)
                QMessageBox.information(self,
                                        "Exito",
                                        "El registor ha sido eliminado correctamente"
                                        )
                self.cargar_combo_box()
            except mysql.connector.Error as error:
                if error.errno == 1451:
                    QMessageBox.critical(
                        self,
                        "Error de integridad referencial",
                        f"No se puede eliminar '{tipo_a_eliminar}' porque esta asociado a uno o más Items "
                    )
                else:
                    QMessageBox.critical(self,"Error DB", f"No se puede eliminar {error}")

            
