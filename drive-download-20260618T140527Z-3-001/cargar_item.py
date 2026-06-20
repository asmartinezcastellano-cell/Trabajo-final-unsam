from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QSpinBox, QDoubleSpinBox, QListWidget,
                               QPushButton, QComboBox, QMessageBox, QScrollArea)

import conexion

class VistaCargarItem(QWidget):
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
        
        label_titulo = QLabel("Registrar Nuevo Item / Producto")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 15px;")
        layout.addWidget(label_titulo)

        layout.addWidget(QLabel("Código de Item (*):"))
        self.input_codigo = QLineEdit()
        self.input_codigo.setMaxLength(10)  
        self.input_codigo.setPlaceholderText("Ej: ART-123")
        layout.addWidget(self.input_codigo)

        layout.addWidget(QLabel("Tipo de Item (Clave Foránea):"))
        self.combo_tipo = QComboBox()
        self.cargar_tipos_items() 
        layout.addWidget(self.combo_tipo)

        layout.addWidget(QLabel("Descripción:"))
        self.input_descripcion = QLineEdit()
        self.input_descripcion.setMaxLength(100)
        layout.addWidget(self.input_descripcion)

        layout.addWidget(QLabel("Color:"))
        self.input_color = QLineEdit()
        self.input_color.setMaxLength(20)
        layout.addWidget(self.input_color)

        # dos columnas
        layout.addWidget(QLabel("<b>Especificaciones Técnicas y Dimensiones:</b>"))
        grid_dimensiones = QHBoxLayout()
        
        # columna izquierda
        col_izq = QVBoxLayout()
        col_izq.addWidget(QLabel("Peso (kg):"))
        self.input_peso = QDoubleSpinBox()
        self.input_peso.setRange(0.0, 99999.99)
        col_izq.addWidget(self.input_peso)

        col_izq.addWidget(QLabel("Ancho (mm):"))
        self.input_ancho = QDoubleSpinBox()
        self.input_ancho.setRange(0.0, 99999.99)
        col_izq.addWidget(self.input_ancho)

        col_izq.addWidget(QLabel("Largo (mm):"))
        self.input_largo = QDoubleSpinBox()
        self.input_largo.setRange(0.0, 99999.99)
        col_izq.addWidget(self.input_largo)
        
        # columna derecha
        col_der = QVBoxLayout()
        col_der.addWidget(QLabel("Diámetro (mm):"))
        self.input_diametro = QDoubleSpinBox()
        self.input_diametro.setRange(0.0, 99999.99)
        col_der.addWidget(self.input_diametro)

        col_der.addWidget(QLabel("Espesor (mm):"))
        self.input_espesor = QDoubleSpinBox()
        self.input_espesor.setRange(0.0, 99999.99)
        col_der.addWidget(self.input_espesor)

        col_der.addWidget(QLabel("Largo Tira/Tubo (mm):"))
        self.input_largo_tira = QDoubleSpinBox()
        self.input_largo_tira.setRange(0.0, 99999.99)
        col_der.addWidget(self.input_largo_tira)

        grid_dimensiones.addLayout(col_izq)
        grid_dimensiones.addLayout(col_der)
        layout.addLayout(grid_dimensiones)

        layout.addWidget(QLabel("Precio Materia Prima ($):"))
        self.input_precio_mp = QDoubleSpinBox()
        self.input_precio_mp.setRange(0.0, 9999999.99)
        layout.addWidget(self.input_precio_mp)

        # --- SECCIÓN: DUAL LISTBOX ---
        layout.addWidget(QLabel("<b>Asignación de Procesos (Obligatorio):</b>"))
        
        dual_list_layout = QHBoxLayout()
        self.lista_disponibles = QListWidget()
        
        botones_medio_layout = QVBoxLayout()
        self.btn_agregar = QPushButton("→")
        self.btn_agregar.setStyleSheet("font-weight: bold; padding: 5px;")
        self.btn_quitar = QPushButton("←")
        self.btn_quitar.setStyleSheet("font-weight: bold; padding: 5px;")
        
        botones_medio_layout.addStretch()
        botones_medio_layout.addWidget(self.btn_agregar)
        botones_medio_layout.addWidget(self.btn_quitar)
        botones_medio_layout.addStretch()
        
        self.lista_seleccionados = QListWidget()
        
        dual_list_layout.addWidget(self.lista_disponibles)
        dual_list_layout.addLayout(botones_medio_layout)
        dual_list_layout.addWidget(self.lista_seleccionados)
        layout.addLayout(dual_list_layout)
       
        self.boton_guardar = QPushButton("Guardar Ítem")
        self.boton_guardar.setStyleSheet("padding: 10px; font-weight: bold; background-color: #4CAF50; color: white;")
        layout.addWidget(self.boton_guardar)
        
        # --- CONEXIONES DE EVENTOS ---
        self.btn_agregar.clicked.connect(self.mover_a_seleccionados)
        self.btn_quitar.clicked.connect(self.mover_a_disponibles)
        self.lista_disponibles.itemDoubleClicked.connect(self.mover_a_seleccionados)
        self.lista_seleccionados.itemDoubleClicked.connect(self.mover_a_disponibles)
        
        # ¡CORRECCIÓN CRÍTICA!: Conectar el botón de guardar a la función
        self.boton_guardar.clicked.connect(self.procesar_guardado)
        
        # Cargar los datos iniciales
        self.cargar_procesos_iniciales()
        layout.addStretch()

    def cargar_tipos_items(self):
        """Busca los tipos de items para rellenar el ComboBox"""
        try:
            tipos = conexion.obtener_todos_los_tipos_item()
            if not tipos:
                self.combo_tipo.addItem("No hay tipos de items disponibles")
                return
            for tipo in tipos:
                self.combo_tipo.addItem(tipo[0])            
        except Exception as e:
            self.combo_tipo.addItem("Error al cargar tipos")
            print(f"Error cargando tipos de item: {e}")

    def limpiar_campos(self):
        self.input_codigo.clear()
        self.input_color.clear()
        self.input_descripcion.clear()
        self.input_peso.setValue(0.0)
        self.input_ancho.setValue(0.0)
        self.input_largo.setValue(0.0)
        self.input_diametro.setValue(0.0)
        self.input_espesor.setValue(0.0)
        self.input_largo_tira.setValue(0.0)
        self.input_precio_mp.setValue(0.0)
        if self.combo_tipo.count() > 0:
            self.combo_tipo.setCurrentIndex(0)
        self.cargar_procesos_iniciales() # Resetea las listas de procesos

    def cargar_procesos_iniciales(self):
        """Llena la lista de la izquierda con los procesos de la BD"""
        try:
            self.lista_disponibles.clear()
            self.lista_seleccionados.clear()
            
            procesos = conexion.obtener_todos_los_tipos_proceso()
            for p in procesos:
                self.lista_disponibles.addItem(p[0])
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los procesos: {e}")

    def mover_a_seleccionados(self):
        item_actual = self.lista_disponibles.currentItem()
        if item_actual:
            self.lista_seleccionados.addItem(item_actual.text())
            self.lista_disponibles.takeItem(self.lista_disponibles.row(item_actual))

    def mover_a_disponibles(self):
        item_actual = self.lista_seleccionados.currentItem()
        if item_actual:
            self.lista_disponibles.addItem(item_actual.text())
            self.lista_seleccionados.takeItem(self.lista_seleccionados.row(item_actual))

    def procesar_guardado(self):
        """Valida, toma los datos reales del formulario y los guarda con sus procesos"""
        codigo = self.input_codigo.text().strip()
        tipo_seleccionado = self.combo_tipo.currentText()

        # 1. Validar Código
        if not codigo:
            QMessageBox.warning(self, "Error de validación", "El campo 'Código de Item' es obligatorio.")
            return

        # 2. Recuperar procesos seleccionados
        procesos_finales = []
        for i in range(self.lista_seleccionados.count()):
            procesos_finales.append(self.lista_seleccionados.item(i).text())
            
        # 3. Validar Procesos Obligatorios
        if not procesos_finales:
            QMessageBox.warning(
                self, 
                "Faltan Procesos", 
                "¡Atención! Debes pasar a la lista de la derecha al menos un proceso para este ítem."
            )
            return 
            
        # 4. Armar los datos reales del formulario (Eliminados los datos fijos de ejemplo)
        datos_item = {
            "codigo_item": codigo,
            "color": self.input_color.text().strip() or None,
            "descripcion": self.input_descripcion.text().strip() or None,
            "peso": self.input_peso.value(),
            "tipo_item": tipo_seleccionado,
            "ancho": self.input_ancho.value(),
            "largo": self.input_largo.value(),
            "diametro": self.input_diametro.value(),
            "espesor": self.input_espesor.value(),
            "largo_tira_tubo": self.input_largo_tira.value(),
            "precio_materia_prima": self.input_precio_mp.value()
        }
        
        try:
            # Enviamos a la función con transacciones que creamos antes
            conexion.guardar_item_con_procesos(datos_item, procesos_finales)
            QMessageBox.information(self, "Éxito", "Ítem registrado con sus procesos correctamente.")
            self.limpiar_campos() 
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudo guardar en la BD: {error}")