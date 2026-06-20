from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QMessageBox)
import conexion

class VistaEliminarProceso(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        
        titulo = QLabel("Eliminar un Proceso")
        titulo.setStyleSheet("font-size : 20px ; font-weight:bold; margin-bottom: 10px; color: #d32f2f;")
        layout.addWidget(titulo)
        
       
        layout.addWidget(QLabel("Seleccione el Proceso que desea eliminar de la base de datos:"))
        self.combo_proceso = QComboBox()
        layout.addWidget(self.combo_proceso)     
        
      
        self.boton_eliminar = QPushButton("Eliminar Proceso")
        self.boton_eliminar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #d32f2f; color: white;")
        self.boton_eliminar.clicked.connect(self.procesar_eliminacion)
        layout.addWidget(self.boton_eliminar)
        
        layout.addStretch()
        self.setLayout(layout)
        
       
        self.cargar_combo_box()

        
    def cargar_combo_box(self):
        
        try:
            self.combo_proceso.clear()
            
            
            registros = conexion.obtener_todos_los_tipos_proceso() 
            
            if registros:
                for fila in registros:
                    self.combo_proceso.addItem(fila[0])
                self.boton_eliminar.setEnabled(True)
            else:
                self.combo_proceso.addItem("No hay procesos registrados")
                self.boton_eliminar.setEnabled(False)
                
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los procesos: {error}")

    def procesar_eliminacion(self):
        """Pide confirmación al usuario y ejecuta el borrado"""
        tipo_seleccionado = self.combo_proceso.currentText()
        
        if not tipo_seleccionado or tipo_seleccionado == "No hay procesos registrados":
            return
            
        # Ventana de advertencia antes de romper la BD
        confirmacion = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Está seguro de que desea eliminar el proceso '{tipo_seleccionado}'?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No # Botón enfocado por defecto por seguridad
        )
        
        if confirmacion == QMessageBox.Yes:
            try:
                # Ejecuta la baja
                conexion.eliminar_proceso_por_tipo(tipo_seleccionado)
                QMessageBox.information(self, "Éxito", f"El proceso '{tipo_seleccionado}' fue eliminado correctamente.")
                
                # Recarga el combobox para que ya no aparezca el elemento borrado
                self.cargar_combo_box()
                
            except Exception as error:
                QMessageBox.critical(self, "Error al eliminar", f"No se pudo completar la operación: {error}")