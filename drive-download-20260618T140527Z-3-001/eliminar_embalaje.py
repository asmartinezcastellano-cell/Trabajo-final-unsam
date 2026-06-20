# ============================================================================
# VISTA PARA ELIMINAR EMBALAJES
# ============================================================================
# Esta clase define la interfaz para eliminar embalajes existentes.
# Incluye confirmación del usuario antes de ejecutar la eliminación.
# ============================================================================

# eliminar_embalaje.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                             QPushButton, QMessageBox)
import mysql.connector
import conexion 

class VistaEliminarEmbalaje(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de eliminación de embalajes.
    #
    # Componentes:
    #   - Título: "Eliminar Embalaje" (en color rojo para advertencia)
    #   - ComboBox: Seleccionar el embalaje a eliminar
    #   - Botón "Eliminar de la Base de Datos": Ejecuta la eliminación
    # ________________________________________________________________________
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

    # ________________________________________________________________________
    # cargar_combo_box()
    # ________________________________________________________________________
    # Carga todos los embalajes disponibles en el ComboBox para selección.
    #
    # Operaciones:
    #   1. Limpia el ComboBox actual
    #   2. Obtiene todos los embalajes de BD
    #   3. Si no hay embalajes: muestra mensaje y desactiva botón
    #   4. Si hay embalajes: los agrega uno por uno y activa botón
    #
    # Se llama cuando se navega a esta pantalla desde el menú.
    # ________________________________________________________________________
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

    # ________________________________________________________________________
    # confirmar_eliminacion()
    # ________________________________________________________________________
    # Solicita confirmación del usuario y procede a eliminar el embalaje.
    #
    # Flujo de ejecución:
    #   1. Obtiene el tipo de embalaje seleccionado
    #   2. Valida que haya selección válida
    #   3. Muestra diálogo de confirmación al usuario (Sí/No)
    #   4. Si el usuario confirma:
    #      a. Llama a conexion.eliminar_embalaje()
    #      b. Muestra mensaje de éxito
    #      c. Recarga la lista de embalajes
    #   5. Si hay error:
    #      - Error 1451: Integridad referencial (embalaje en uso)
    #      - Otros: Muestra mensaje de error genérico
    #
    # Nota: Usa confirmación para evitar eliminaciones accidentales.
    # ________________________________________________________________________
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