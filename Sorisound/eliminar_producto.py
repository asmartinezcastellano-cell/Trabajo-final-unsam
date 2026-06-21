from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QComboBox, QMessageBox, QScrollArea, QAbstractItemView, QHeaderView)
import conexion

#==========================================================================
#MODULO: eliminar_producto.py
#DESCRIPCION: Formulario para eliminar productos registrados en la BD
#Muestra combo box con productos disponibles, confirma eliminación y maneja errores
#
#FUNCIONALIDADES:
# - Carga productos disponibles en combo box al abrir la vista
# - Permite seleccionar un producto y eliminarlo de la BD
# - Muestra tabla con información del producto antes de eliminar
# - Muestra mensajes de confirmación y error según corresponda
#
#NOTAS:
# - Al eliminar un producto, se eliminan también sus ítems asociados
# - La eliminación no se permite si hay restricciones de integridad
#
#==========================================================================

class VistaEliminarProducto(QWidget):
    def __init__(self):
        super().__init__()        
        
        layout_principal = QVBoxLayout(self)
        
        label_titulo = QLabel("Eliminar Producto del Sistema")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 15px; color: #C62828;")
        layout_principal.addWidget(label_titulo)

        # --- SELECCIÓN DEL PRODUCTO ---
        layout_principal.addWidget(QLabel("<b>Seleccione el modelo del producto que desea remover:</b>"))
        self.combo_modelo = QComboBox()
        self.combo_modelo.setStyleSheet("padding: 5px; font-weight: bold;")
        layout_principal.addWidget(self.combo_modelo)
        
        # Conectar cambio de selección para previsualizar automáticamente
        self.combo_modelo.currentTextChanged.connect(self.previsualizar_producto)

        layout_principal.addWidget(QLabel("<hr>"))

        # --- PANEL DE VISTA PREVIA (INFORMACIÓN GENERAL) ---
        layout_principal.addWidget(QLabel("<b>Información del Producto Seleccionado:</b>"))
        
        self.lbl_descripcion = QLabel("Descripción: -")
        self.lbl_color = QLabel("Color: -")
        self.lbl_embalaje = QLabel("Embalaje: -")
        
        layout_principal.addWidget(self.lbl_descripcion)
        layout_principal.addWidget(self.lbl_color)
        layout_principal.addWidget(self.lbl_embalaje)

        # --- TABLA DE COMPONENTES AFECTADOS ---
        layout_principal.addWidget(QLabel("<b>Ítems componentes que perderán la vinculación:</b>"))
        self.tabla_items = QTableWidget(0, 2)
        self.tabla_items.setHorizontalHeaderLabels(["Código de Ítem", "Cantidad"])
        self.tabla_items.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_items.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_items.setStyleSheet("QTableWidget { background-color: #FDF2F2; }")
        layout_principal.addWidget(self.tabla_items)

        # --- BOTÓN DE ELIMINACIÓN ---
        self.btn_eliminar = QPushButton("❌ Eliminar Producto Definitivamente")
        self.btn_eliminar.setStyleSheet("padding: 12px; font-weight: bold; background-color: #D32F2F; color: white; margin-top: 10px;")
        self.btn_eliminar.clicked.connect(self.procesar_eliminacion)
        layout_principal.addWidget(self.btn_eliminar)

        # Carga inicial del combo
        self.cargar_modelos_disponibles()

    def cargar_modelos_disponibles(self):
        """Puebla el ComboBox con todos los productos de la BD"""
        try:
            # Desconectar temporalmente la señal para evitar disparos en cascada al limpiar
            self.combo_modelo.currentTextChanged.disconnect()
            
            self.combo_modelo.clear()
            productos = conexion.obtener_todos_los_modelos_producto()
            
            if not productos:
                self.combo_modelo.addItem("No hay productos en el sistema")
                self.btn_eliminar.setEnabled(False)
            else:
                self.btn_eliminar.setEnabled(True)
                for prod in productos:
                    self.combo_modelo.addItem(prod[0])
            
            # Reconectar la señal e invocar la primera previsualización manualmente
            self.combo_modelo.currentTextChanged.connect(self.previsualizar_producto)
            self.previsualizar_producto(self.combo_modelo.currentText())
            
        except Exception as e:
            print(f"Error cargando los modelos: {e}")

    def previsualizar_producto(self, modelo):
        """Muestra los datos y componentes del producto seleccionado antes de borrarlo"""
        if not modelo or modelo == "No hay productos en el sistema":
            self.lbl_descripcion.setText("Descripción: -")
            self.lbl_color.setText("Color: -")
            self.lbl_embalaje.setText("Embalaje: -")
            self.tabla_items.setRowCount(0)
            return

        try:
            # 1. Buscar datos generales
            prod_info = conexion.obtener_producto_por_modelo(modelo)
            if prod_info:
                self.lbl_descripcion.setText(f"<b>Descripción:</b> {prod_info[1] or 'Sin descripción'}")
                self.lbl_color.setText(f"<b>Color:</b> {prod_info[2] or 'No especificado'}")
                self.lbl_embalaje.setText(f"<b>Embalaje asignado:</b> {prod_info[3] or 'Ninguno'}")

            # 2. Buscar los ítems asociados en la tabla
            items_asociados = conexion.obtener_items_por_modelo_producto(modelo)
            self.tabla_items.setRowCount(0)
            
            for fila_idx, (codigo_item, cantidad) in enumerate(items_asociados):
                self.tabla_items.insertRow(fila_idx)
                self.tabla_items.setItem(fila_idx, 0, QTableWidgetItem(str(codigo_item)))
                self.tabla_items.setItem(fila_idx, 1, QTableWidgetItem(str(cantidad)))

        except Exception as e:
            print(f"Error en la previsualización: {e}")

    def procesar_eliminacion(self):
        """Valida y ejecuta la baja definitiva del producto"""
        modelo = self.combo_modelo.currentText()
        if not modelo or modelo == "No hay productos en el sistema":
            return

        # Primer aviso de seguridad
        respuesta = QMessageBox.question(
            self,
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar el producto '{modelo}'?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            try:
                # Ejecutar borrado transaccional
                conexion.eliminar_producto_por_modelo(modelo)
                QMessageBox.information(self, "Éxito", f"El producto '{modelo}' fue removido con éxito.")
                
                # Refrescar la ventana
                self.cargar_modelos_disponibles()
            except Exception as error:
                QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {error}")