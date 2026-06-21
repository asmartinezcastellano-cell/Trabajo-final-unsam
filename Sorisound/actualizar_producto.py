from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QSpinBox, QListWidget, QTableWidget,
                               QTableWidgetItem, QPushButton, QComboBox, 
                               QMessageBox, QScrollArea, QAbstractItemView)
from PySide6.QtCore import Qt
import conexion

#==========================================================================
#MODULO: actualizar_producto.py
#DESCRIPCION: Formulario para modificar un producto existente en la BD
#Permite editar descripción, color, embalaje y los ítems asociados
#Validación de campos, manejo de errores y feedback de usuario
#
#FUNCIONALIDADES:
# - Carga lista de productos disponibles en combo box al abrir la vista
# - Al seleccionar un producto, muestra sus datos actuales
# - Permite modificar descripción, color y tipo de embalaje
# - Permite agregar/remover ítems asociados al producto
# - Valida campos antes de guardar cambios en BD
# - Muestra mensajes de confirmación y error según corresponda
#
#NOTAS:
# - Los cambios se guardan inmediatamente en la BD
# - Se valida que los campos no estén vacíos
# - Se mantiene sincronización con la lista de ítems disponibles
#
#==========================================================================


class VistaModificarProducto(QWidget):
    def __init__(self):
        super().__init__()        
        
        scroll_layout = QVBoxLayout()
        self.setLayout(scroll_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_layout.addWidget(scroll)
        
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        scroll.setWidget(contenedor)
        
        label_titulo = QLabel("Modificar Producto Existente")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 15px; color: #E65100;")
        layout.addWidget(label_titulo)

        # --- SELECCIÓN DEL PRODUCTO A MODIFICAR ---
        layout.addWidget(QLabel("<b>Seleccione el Producto a Modificar:</b>"))
        self.combo_buscar_modelo = QComboBox()
        self.combo_buscar_modelo.setStyleSheet("padding: 5px; font-weight: bold;")
        layout.addWidget(self.combo_buscar_modelo)
        
        self.btn_cargar = QPushButton("Cargar Datos del Producto")
        self.btn_cargar.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold; padding: 6px;")
        layout.addWidget(self.btn_cargar)

        layout.addWidget(QLabel("<hr>"))

        # --- CAMPOS EDITABLES ---
        layout.addWidget(QLabel("Descripción:"))
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setMaxLength(100)
        layout.addWidget(self.input_descripcion)

        layout.addWidget(QLabel("Color:"))
        self.input_color = QLineEdit()
        self.input_color.setMaxLength(20)
        layout.addWidget(self.input_color)

        layout.addWidget(QLabel("Tipo de Embalaje:"))
        self.combo_embalaje = QComboBox()
        layout.addWidget(self.combo_embalaje)

        # --- SECCIÓN: EDICIÓN DE ÍTEMS Y CANTIDADES ---
        layout.addWidget(QLabel("<b>Modificar Ítems y Cantidades Asociadas:</b>"))
        
        seccion_items_layout = QHBoxLayout()
        
        # Panel Izquierdo: Disponibles
        panel_izq = QVBoxLayout()
        panel_izq.addWidget(QLabel("Ítems Disponibles (No usados):"))
        self.lista_disponibles = QListWidget()
        panel_izq.addWidget(self.lista_disponibles)
        seccion_items_layout.addLayout(panel_izq)
        
        # Panel Central: Control de flujo
        botones_medio_layout = QVBoxLayout()
        botones_medio_layout.addStretch()
        botones_medio_layout.addWidget(QLabel("Cantidad:"))
        self.spin_cantidad = QSpinBox()
        self.spin_cantidad.setRange(1, 9999)
        self.spin_cantidad.setValue(1)
        botones_medio_layout.addWidget(self.spin_cantidad)
        
        self.btn_agregar = QPushButton("Añadir →")
        self.btn_agregar.setStyleSheet("font-weight: bold; padding: 5px;")
        botones_medio_layout.addWidget(self.btn_agregar)
        
        self.btn_quitar = QPushButton("← Quitar")
        self.btn_quitar.setStyleSheet("font-weight: bold; padding: 5px;")
        botones_medio_layout.addWidget(self.btn_quitar)
        botones_medio_layout.addStretch()
        seccion_items_layout.addLayout(botones_medio_layout)
        
        # Panel Derecho: Tabla del Producto
        panel_der = QVBoxLayout()
        panel_der.addWidget(QLabel("Ítems definidos en este Producto:"))
        self.tabla_seleccionados = QTableWidget(0, 2)
        self.tabla_seleccionados.setHorizontalHeaderLabels(["Código de Ítem", "Cantidad"])
        self.tabla_seleccionados.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_seleccionados.setSelectionMode(QAbstractItemView.SingleSelection)
        panel_der.addWidget(self.tabla_seleccionados)
        seccion_items_layout.addLayout(panel_der)
        
        layout.addLayout(seccion_items_layout)
       
        # --- BOTÓN GUARDAR CAMBIOS ---
        self.boton_guardar = QPushButton("Guardar Cambios en Producto")
        self.boton_guardar.setStyleSheet("padding: 10px; font-weight: bold; background-color: #4CAF50; color: white;")
        layout.addWidget(self.boton_guardar)
        
        # --- CONEXIONES ---
        self.btn_cargar.clicked.connect(self.cargar_datos_producto_seleccionado)
        self.btn_agregar.clicked.connect(self.agregar_item_a_tabla)
        self.btn_quitar.clicked.connect(self.quitar_item_de_tabla)
        self.boton_guardar.clicked.connect(self.procesar_guardado)
        
        # Inicializar combos y listas de base
        self.actualizar_combos_iniciales()
        layout.addStretch()
    
    # ==========================================================================
    # FUNCIONES DE APOYO PARA CARGA Y PROCESAMIENTO DE DATOS
    # ==========================================================================

    def actualizar_combos_iniciales(self):
        """Llena los selectores de productos y embalajes"""
        try:
            # 1. Cargar Modelos de Productos disponibles para editar
            self.combo_buscar_modelo.clear()
            productos = conexion.obtener_todos_los_modelos_producto()
            for prod in productos:
                self.combo_buscar_modelo.addItem(prod[0])
                
            # 2. Cargar Embalajes
            self.combo_embalaje.clear()
            embalajes = conexion.obtener_todos_los_embalajes_combo()
            for emb in embalajes:
                self.combo_embalaje.addItem(emb[0])
        except Exception as e:
            print(f"Error cargando iniciales: {e}")

    def cargar_datos_producto_seleccionado(self):
        """Busca el producto y sus relaciones para plasmarlo en la GUI"""
        modelo = self.combo_buscar_modelo.currentText()
        if not modelo:
            QMessageBox.warning(self, "Atención", "No hay ningún modelo seleccionado.")
            return
            
        try:
            # 1. Obtener datos base
            prod_info = conexion.obtener_producto_por_modelo(modelo)
            if prod_info:
                self.input_descripcion.setText(prod_info[1] or "")
                self.input_color.setText(prod_info[2] or "")
                idx_emb = self.combo_embalaje.findText(prod_info[3] or "")
                if idx_emb != -1:
                    self.combo_embalaje.setCurrentIndex(idx_emb)
            
            # 2. Obtener los ítems que ya posee el producto
            items_asignados = conexion.obtener_items_por_modelo_producto(modelo)
            codigos_asignados = [rel[0] for rel in items_asignados]
            
            # 3. Limpiar y estructurar la Tabla de seleccionados
            self.tabla_seleccionados.setRowCount(0)
            for cod, cant in items_asignados:
                fila_idx = self.tabla_seleccionados.rowCount()
                self.tabla_seleccionados.insertRow(fila_idx)
                self.tabla_seleccionados.setItem(fila_idx, 0, QTableWidgetItem(cod))
                self.tabla_seleccionados.setItem(fila_idx, 1, QTableWidgetItem(str(cant)))
                
            # 4. Cargar en la lista de la izquierda SOLO los ítems de la BD que NO use este producto actualmente
            self.lista_disponibles.clear()
            todos_los_items = conexion.obtener_todos_los_codigos_item()
            for item in todos_los_items:
                if item[0] not in codigos_asignados:
                    self.lista_disponibles.addItem(item[0])
                    
            QMessageBox.information(self, "Carga Exitosa", f"Datos del modelo '{modelo}' cargados correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron recuperar los datos: {e}")

    def agregar_item_a_tabla(self):
        item_actual = self.lista_disponibles.currentItem()
        if not item_actual:
            QMessageBox.warning(self, "Atención", "Selecciona un ítem libre de la lista izquierda.")
            return
        
        codigo = item_actual.text()
        cantidad = self.spin_cantidad.value()
        
        fila_idx = self.tabla_seleccionados.rowCount()
        self.tabla_seleccionados.insertRow(fila_idx)
        self.tabla_seleccionados.setItem(fila_idx, 0, QTableWidgetItem(codigo))
        self.tabla_seleccionados.setItem(fila_idx, 1, QTableWidgetItem(str(cantidad)))
        
        self.lista_disponibles.takeItem(self.lista_disponibles.row(item_actual))
        self.spin_cantidad.setValue(1)

    def quitar_item_de_tabla(self):
        fila_actual = self.tabla_seleccionados.currentRow()
        if fila_actual == -1:
            QMessageBox.warning(self, "Atención", "Selecciona una fila de la tabla para dar de baja.")
            return
            
        codigo = self.tabla_seleccionados.item(fila_actual, 0).text()
        self.lista_disponibles.addItem(codigo)
        self.tabla_seleccionados.removeRow(fila_actual)

    def limpiar_formulario(self):
        self.input_descripcion.clear()
        self.input_color.clear()
        self.tabla_seleccionados.setRowCount(0)
        self.lista_disponibles.clear()
        self.actualizar_combos_iniciales()

    def procesar_guardado(self):
        modelo = self.combo_buscar_modelo.currentText()
        if not modelo:
            return

        items_finales = []
        for fila in range(self.tabla_seleccionados.rowCount()):
            cod = self.tabla_seleccionados.item(fila, 0).text()
            cant = int(self.tabla_seleccionados.item(fila, 1).text())
            items_finales.append({"codigo_item": cod, "cantidad": cant})
            
        if not items_finales:
            QMessageBox.warning(self, "Faltan Ítems", "El producto no puede quedar vacío. Asigna al menos un ítem.")
            return 
            
        datos_producto = {
            "modelo": modelo,
            "descripcion": self.input_descripcion.text().strip() or None,
            "color": self.input_color.text().strip() or None,
            "embalaje": self.combo_embalaje.currentText() or None
        }
        
        try:
            conexion.actualizar_producto_con_items(datos_producto, items_finales)
            QMessageBox.information(self, "Éxito", "Producto actualizado correctamente en el sistema.")
            self.limpiar_formulario()
        except Exception as error:
            QMessageBox.critical(self, "Error", f"Error al intentar impactar los cambios: {error}")