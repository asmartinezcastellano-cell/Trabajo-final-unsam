from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QSpinBox, QListWidget, QTableWidget,
                               QTableWidgetItem, QPushButton, QComboBox, 
                               QMessageBox, QScrollArea, QAbstractItemView)
from PySide6.QtCore import Qt
import conexion

#==========================================================================
#MODULO: cargar_producto.py
#DESCRIPCION: Formulario para registrar nuevos productos en la BD
#Incluye validación de campos, manejo de errores y feedback de usuario
#
#FUNCIONALIDADES:
# - Formulario para ingresar datos de un nuevo producto (modelo, descripción, color, embalaje)
# - Permite seleccionar e incluir ítems asociados al producto
# - Valida que los campos no estén vacíos y tengan valores válidos
# - Verifica que el código del producto sea único en la BD
# - Guarda el nuevo producto en la BD con sus ítems asociados
# - Muestra mensajes de confirmación y error según corresponda
#
#NOTAS:
# - No se permite registrar productos con el mismo código
# - El producto debe tener al menos un ítem asociado
# - Se valida que el embalaje seleccionado exista en la BD
#
#==========================================================================


class VistaCargarProducto(QWidget):
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
        
        label_titulo = QLabel("Registrar Nuevo Producto")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 15px;")
        layout.addWidget(label_titulo)

        # --- CAMPOS DEL PRODUCTO ---
        layout.addWidget(QLabel("Modelo de Producto (*):"))
        self.input_modelo = QLineEdit()
        self.input_modelo.setMaxLength(50)  
        self.input_modelo.setPlaceholderText("Ej: MESA-ESC-01")
        layout.addWidget(self.input_modelo)

        layout.addWidget(QLabel("Descripción:"))
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setMaxLength(100)
        layout.addWidget(self.input_descripcion)

        layout.addWidget(QLabel("Color:"))
        self.input_color = QLineEdit()
        self.input_color.setMaxLength(20)
        layout.addWidget(self.input_color)

        layout.addWidget(QLabel("Tipo de Embalaje (Clave Foránea):"))
        self.combo_embalaje = QComboBox()
        self.cargar_embalajes() 
        layout.addWidget(self.combo_embalaje)

        # --- SECCIÓN: ASIGNACIÓN DE ÍTEMS CON CANTIDAD ---
        layout.addWidget(QLabel("<b>Asignación de Ítems y Cantidades (Obligatorio):</b>"))
        
        seccion_items_layout = QHBoxLayout()
        
        # Panel Izquierdo: Ítems Disponibles
        panel_izq = QVBoxLayout()
        panel_izq.addWidget(QLabel("Ítems Disponibles:"))
        self.lista_disponibles = QListWidget()
        panel_izq.addWidget(self.lista_disponibles)
        seccion_items_layout.addLayout(panel_izq)
        
        # Panel Central: Selector de Cantidad y Botones
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
        
        # Panel Derecho: Tabla de Ítems Seleccionados
        panel_der = QVBoxLayout()
        panel_der.addWidget(QLabel("Ítems en este Producto:"))
        self.tabla_seleccionados = QTableWidget(0, 2)
        self.tabla_seleccionados.setHorizontalHeaderLabels(["Código de Ítem", "Cantidad"])
        self.tabla_seleccionados.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_seleccionados.setSelectionMode(QAbstractItemView.SingleSelection)
        panel_der.addWidget(self.tabla_seleccionados)
        seccion_items_layout.addLayout(panel_der)
        
        layout.addLayout(seccion_items_layout)
       
        # --- BOTÓN GUARDAR ---
        self.boton_guardar = QPushButton("Guardar Producto")
        self.boton_guardar.setStyleSheet("padding: 10px; font-weight: bold; background-color: #2196F3; color: white;")
        layout.addWidget(self.boton_guardar)
        
        # --- CONEXIONES DE EVENTOS ---
        self.btn_agregar.clicked.connect(self.agregar_item_a_tabla)
        self.btn_quitar.clicked.connect(self.quitar_item_de_tabla)
        self.boton_guardar.clicked.connect(self.procesar_guardado)
        
        # Cargar los datos iniciales
        self.cargar_items_disponibles()
        layout.addStretch()

    def cargar_embalajes(self):
        """Puebla el ComboBox con los tipos de embalaje desde la BD"""
        try:
            self.combo_embalaje.clear()
            embalajes = conexion.obtener_todos_los_embalajes_combo()
            if not embalajes:
                self.combo_embalaje.addItem("No hay embalajes disponibles")
                return
            for emb in embalajes:
                self.combo_embalaje.addItem(emb[0])            
        except Exception as e:
            self.combo_embalaje.addItem("Error al cargar embalajes")
            print(f"Error cargando embalajes: {e}")

    def cargar_items_disponibles(self):
        """Llena la lista de la izquierda con los códigos de ítem de la BD"""
        try:
            self.lista_disponibles.clear()
            items = conexion.obtener_todos_los_codigos_item()
            for item in items:
                self.lista_disponibles.addItem(item[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los ítems: {e}")

    def agregar_item_a_tabla(self):
        """Pasa el ítem seleccionado con la cantidad indicada a la tabla derecha"""
        item_actual = self.lista_disponibles.currentItem()
        if not item_actual:
            QMessageBox.warning(self, "Atención", "Selecciona un ítem de la lista izquierda.")
            return
        
        codigo = item_actual.text()
        cantidad = self.spin_cantidad.value()
        
        # Verificar si el ítem ya está agregado para sumar cantidades en lugar de duplicar fila
        for fila in range(self.tabla_seleccionados.rowCount()):
            if self.tabla_seleccionados.item(fila, 0).text() == codigo:
                cant_actual = int(self.tabla_seleccionados.item(fila, 1).text())
                self.tabla_seleccionados.setItem(fila, 1, QTableWidgetItem(str(cant_actual + cantidad)))
                # Remover de la lista si ya no se quiere disponible o dejarlo por si se quiere añadir más
                return

        # Si es nuevo, añadimos la fila
        fila_idx = self.tabla_seleccionados.rowCount()
        self.tabla_seleccionados.insertRow(fila_idx)
        self.tabla_seleccionados.setItem(fila_idx, 0, QTableWidgetItem(codigo))
        self.tabla_seleccionados.setItem(fila_idx, 1, QTableWidgetItem(str(cantidad)))
        
        # Opcional: remover de la lista de disponibles
        self.lista_disponibles.takeItem(self.lista_disponibles.row(item_actual))
        self.spin_cantidad.setValue(1)

    def quitar_item_de_tabla(self):
        """Remueve el ítem de la tabla y lo regresa a la lista de disponibles"""
        fila_actual = self.tabla_seleccionados.currentRow()
        if fila_actual == -1:
            QMessageBox.warning(self, "Atención", "Selecciona una fila de la tabla para quitar.")
            return
            
        codigo = self.tabla_seleccionados.item(fila_actual, 0).text()
        
        # Devolver a la lista de la izquierda
        self.lista_disponibles.addItem(codigo)
        # Eliminar fila
        self.tabla_seleccionados.removeRow(fila_actual)

    def limpiar_campos(self):
        self.input_modelo.clear()
        self.input_descripcion.clear()
        self.input_color.clear()
        if self.combo_embalaje.count() > 0:
            self.combo_embalaje.setCurrentIndex(0)
        self.tabla_seleccionados.setRowCount(0)
        self.cargar_items_disponibles()
        self.spin_cantidad.setValue(1)

    def procesar_guardado(self):
        """Valida y estructura los datos para enviarlos a la base de datos"""
        modelo = self.input_modelo.text().strip()
        embalaje_seleccionado = self.combo_embalaje.currentText()

        if not modelo:
            QMessageBox.warning(self, "Error de validación", "El campo 'Modelo de Producto' es obligatorio.")
            return

        # Recuperar ítems y cantidades desde la tabla
        items_finales = []
        for fila in range(self.tabla_seleccionados.rowCount()):
            cod = self.tabla_seleccionados.item(fila, 0).text()
            cant = int(self.tabla_seleccionados.item(fila, 1).text())
            items_finales.append({"codigo_item": cod, "cantidad": cant})
            
        if not items_finales:
            QMessageBox.warning(
                self, 
                "Faltan Ítems", 
                "¡Atención! El producto debe tener asignado al menos un ítem con su cantidad."
            )
            return 
            
        datos_producto = {
            "modelo": modelo,
            "descripcion": self.input_descripcion.text().strip() or None,
            "color": self.input_color.text().strip() or None,
            "embalaje": embalaje_seleccionado if embalaje_seleccionado != "No hay embalajes disponibles" else None
        }
        
        try:
            conexion.guardar_producto_con_items(datos_producto, items_finales)
            QMessageBox.information(self, "Éxito", "Producto registrado correctamente con sus componentes.")
            self.limpiar_campos() 
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el producto en la BD: {error}")