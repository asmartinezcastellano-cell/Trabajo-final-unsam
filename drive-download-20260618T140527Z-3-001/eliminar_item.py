from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QComboBox, 
                               QPushButton, QMessageBox, QFrame)
import conexion

# ============================================================================
# VISTA PARA ELIMINAR ITEMS EXISTENTES
# ============================================================================
# Esta clase define la interfaz para eliminar items/productos del catálogo.
# Incluye múltiples confirmaciones de seguridad para evitar eliminaciones 
# accidentales.
# ============================================================================

class VistaEliminarItem(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de eliminación de items.
    #
    # Componentes:
    #   - Título: "Eliminar Ítem del Sistema" (en rojo para advertencia)
    #   - Marco de selección: ComboBox con códigos de items
    #   - Botón rojo: "🚨 Eliminar Definitivamente"
    #
    # Se ejecuta refrescar_selector() al inicializar para cargar los códigos.
    # ________________________________________________________________________
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout(self)
        
        
        label_titulo = QLabel("Eliminar Ítem del Sistema")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; color: #c0392b; margin-bottom: 15px;")
        layout.addWidget(label_titulo)
        
        
        frame_seleccion = QFrame()
        frame_seleccion.setFrameShape(QFrame.StyledPanel)
        layout_interno = QVBoxLayout(frame_seleccion)
        
        layout_interno.addWidget(QLabel("<b>Seleccione el Código del Ítem que desea borrar:</b>"))
        self.combo_eliminar = QComboBox()
        layout_interno.addWidget(self.combo_eliminar)
        
        layout.addWidget(frame_seleccion)
        
        
        self.boton_eliminar = QPushButton("🚨 Eliminar Definitivamente")
        self.boton_eliminar.setStyleSheet("padding: 12px; background-color: #e74c3c; color: white; font-weight: bold; font-size: 14px; margin-top: 15px;")
        self.boton_eliminar.clicked.connect(self.procesar_eliminacion)
        layout.addWidget(self.boton_eliminar)
        
        layout.addStretch()
        
        
        self.refrescar_selector()
    
    # ________________________________________________________________________
    # refrescar_selector()
    # ________________________________________________________________________
    # Carga todos los códigos de items disponibles en el ComboBox.
    #
    # Operaciones:
    #   1. Limpia el ComboBox actual
    #   2. Obtiene todos los códigos de items de BD
    #   3. Si no hay items: muestra mensaje "No hay ítems registrados"
    #   4. Si hay items: agrega cada código al ComboBox
    #
    # Se ejecuta en __init__() y después de cada eliminación exitosa.
    # ________________________________________________________________________
    def refrescar_selector(self):
        """Llena el ComboBox con los códigos actuales de la BD"""
        self.combo_eliminar.clear()
        try:
            
            codigos = conexion.obtener_todos_los_codigos_item()
            if not codigos:
                self.combo_eliminar.addItem("No hay ítems registrados")
                return
            for c in codigos:
                self.combo_eliminar.addItem(c[0])
        except Exception as e:
            print(f"Error al cargar códigos para eliminar: {e}")

    # ________________________________________________________________________
    # procesar_eliminacion()
    # ________________________________________________________________________
    # Solicita confirmación del usuario y procede a eliminar el item.
    #
    # Validaciones de seguridad:
    #   1. Verifica que haya un item válido seleccionado
    #   2. Solicita confirmación explícita del usuario (con botón "No" por defecto)
    #
    # Flujo de ejecución:
    #   1. Obtiene el código del item seleccionado
    #   2. Valida que no esté vacío
    #   3. Muestra diálogo de confirmación (Sí/No)
    #   4. Si el usuario confirma:
    #      a. Llama a conexion.eliminar_item_por_codigo()
    #      b. Muestra mensaje de éxito
    #      c. Recarga la lista de códigos
    #   5. Si hay error: muestra detalles del error
    #
    # Nota: Usa confirmación doble para evitar eliminaciones accidentales.
    # ________________________________________________________________________
    def procesar_eliminacion(self):
        codigo_seleccionado = self.combo_eliminar.currentText()
        
       #verificamos si la bd esta vacia
        if not codigo_seleccionado or codigo_seleccionado == "No hay ítems registrados":
            QMessageBox.warning(self, "Operación inválida", "No hay ningún ítem seleccionado para eliminar.")
            return
            
       # Pedimos una confirmación adicional al usuario antes de eliminar, para evitar eliminaciones accidentales
        confirmacion = QMessageBox.question(
            self, 
            "Confirmar Eliminación", 
            f"¿Está absolutamente seguro de que desea eliminar el ítem '{codigo_seleccionado}'?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No # El botón "No" viene seleccionado por defecto por seguridad
        )
        # Si el usuario confirma la eliminación, procedemos a eliminar el ítem de la base de datos
        if confirmacion == QMessageBox.Yes:
            try:
                conexion.eliminar_item_por_codigo(codigo_seleccionado)
                QMessageBox.information(self, "Éxito", f"El ítem '{codigo_seleccionado}' fue eliminado correctamente.")
                
                #refresco la lista para que no aparezca el codigo recien borrado
                self.refrescar_selector()
                
            except Exception as e:
                # aparece error de clave foranea
                QMessageBox.critical(self, "Error al eliminar", f"No se pudo eliminar el ítem.\nDetalle: {e}")