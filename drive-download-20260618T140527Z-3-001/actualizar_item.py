from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QDoubleSpinBox, QPushButton, QListWidget,
                               QComboBox, QMessageBox, QScrollArea, QFrame)
import conexion

class VistaModificarItem(QWidget):
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout(self)
        self.bloquear_senal = False # Bandera de control para cargas de datos
        
        # Parte superior de la ventana (Filtro/Búsqueda)
        frame_busqueda = QFrame()
        frame_busqueda.setFrameShape(QFrame.StyledPanel)
        layout_busqueda = QVBoxLayout(frame_busqueda)
        
        layout_busqueda.addWidget(QLabel("<b>Seleccione el Código del Item a modificar:</b>"))
        self.combo_selector = QComboBox()       
        self.combo_selector.currentTextChanged.connect(self.cargar_datos_del_item)
        layout_busqueda.addWidget(self.combo_selector)
        
        layout_principal.addWidget(frame_busqueda)

        # Scroll Area para el Formulario
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout_principal.addWidget(scroll)
        
        contenedor = QWidget()
        self.layout_form = QVBoxLayout(contenedor)
        scroll.setWidget(contenedor)

        self.layout_form.addWidget(QLabel("<h3>Detalles del Item</h3>"))

        self.layout_form.addWidget(QLabel("Tipo de Item:"))
        self.combo_tipo = QComboBox()
        self.cargar_tipos_en_combo() 
        self.layout_form.addWidget(self.combo_tipo)

        self.layout_form.addWidget(QLabel("Descripción:"))
        self.input_descripcion = QLineEdit()
        self.layout_form.addWidget(self.input_descripcion)

        self.layout_form.addWidget(QLabel("Color:"))
        self.input_color = QLineEdit()
        self.layout_form.addWidget(self.input_color)

        # Grilla de Dimensiones (Dos Columnas)
        grid_dim = QHBoxLayout()
        col_izq = QVBoxLayout()
        self.input_peso = QDoubleSpinBox(); self.input_peso.setRange(0, 99999)
        col_izq.addWidget(QLabel("Peso (kg):")); col_izq.addWidget(self.input_peso)
        self.input_ancho = QDoubleSpinBox(); self.input_ancho.setRange(0, 99999)
        col_izq.addWidget(QLabel("Ancho (mm):")); col_izq.addWidget(self.input_ancho)
        self.input_largo = QDoubleSpinBox(); self.input_largo.setRange(0, 99999)
        col_izq.addWidget(QLabel("Largo (mm):")); col_izq.addWidget(self.input_largo)

        col_der = QVBoxLayout()
        self.input_diametro = QDoubleSpinBox(); self.input_diametro.setRange(0, 99999)
        col_der.addWidget(QLabel("Diámetro (mm):")); col_der.addWidget(self.input_diametro)
        self.input_espesor = QDoubleSpinBox(); self.input_espesor.setRange(0, 99999)
        col_der.addWidget(QLabel("Espesor (mm):")); col_der.addWidget(self.input_espesor)
        self.input_largo_tira = QDoubleSpinBox(); self.input_largo_tira.setRange(0, 99999)
        col_der.addWidget(QLabel("Largo Tira (mm):")); col_der.addWidget(self.input_largo_tira)

        grid_dim.addLayout(col_izq)
        grid_dim.addLayout(col_der)
        self.layout_form.addLayout(grid_dim)

        self.layout_form.addWidget(QLabel("Precio Materia Prima ($):"))
        self.input_precio_mp = QDoubleSpinBox()
        self.input_precio_mp.setRange(0, 9999999)
        self.layout_form.addWidget(self.input_precio_mp)

        # --- SECCIÓN NUEVA: DUAL LISTBOX ---
        self.layout_form.addWidget(QLabel("<b>Asignación de Procesos (Obligatorio):</b>"))
        
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
        self.layout_form.addLayout(dual_list_layout)
        
        # --- BOTÓN DE ACCIÓN ---
        self.boton_actualizar = QPushButton("Actualizar Datos en Base de Datos")
        self.boton_actualizar.setStyleSheet("padding: 10px; background-color: #f39c12; color: white; font-weight: bold;")
        self.layout_form.addWidget(self.boton_actualizar)
        
        self.layout_form.addStretch()

        # --- CONEXIONES DE EVENTOS ---
        self.btn_agregar.clicked.connect(self.mover_a_seleccionados)
        self.btn_quitar.clicked.connect(self.mover_a_disponibles)
        self.lista_disponibles.itemDoubleClicked.connect(self.mover_a_seleccionados)
        self.lista_seleccionados.itemDoubleClicked.connect(self.mover_a_disponibles)
        self.boton_actualizar.clicked.connect(self.procesar_actualizacion)
        
        # Cargar selectores iniciales
        self.refrescar_selectores()

    def refrescar_selectores(self):
        """Llena el combo superior con los códigos existentes"""
        try:
            self.bloquear_senal = True
            self.combo_selector.clear()
            codigos = conexion.obtener_todos_los_codigos_item()
            for c in codigos:
                self.combo_selector.addItem(c[0])
            self.bloquear_senal = False
            
            if self.combo_selector.count() > 0:
                self.cargar_datos_del_item(self.combo_selector.currentText())
        except Exception as e:
            print(f"Error cargando selectores: {e}")

    def cargar_tipos_en_combo(self):
        try:
            tipos = conexion.obtener_todos_los_tipos_item()
            for t in tipos:
                self.combo_tipo.addItem(t[0])
        except Exception as e:
            print(f"Error cargando tipos: {e}")

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

    def cargar_datos_del_item(self, codigo):
        """Setea los campos e inicializa las listas cruzando los procesos asignados"""
        if self.bloquear_senal or not codigo: 
            return
        
        try:
            item = conexion.obtener_item_por_codigo(codigo)
            if item:
                # Cargar inputs tradicionales
                self.input_color.setText(item[1] or "")
                self.input_descripcion.setText(item[2] or "")
                self.input_peso.setValue(item[3])
               
                index = self.combo_tipo.findText(item[4])
                self.combo_tipo.setCurrentIndex(index)
                self.input_ancho.setValue(item[5])
                self.input_largo.setValue(item[6])
                self.input_diametro.setValue(item[7])
                self.input_espesor.setValue(item[8])
                self.input_largo_tira.setValue(item[9])
                self.input_precio_mp.setValue(item[10])
                
                # --- Sincronización del Dual Listbox ---
                self.lista_disponibles.clear()
                self.lista_seleccionados.clear()
                
                # Traer los procesos que YA tiene asignados este ítem
                procesos_asignados = conexion.obtener_procesos_por_codigo_item(codigo)
                # Traer TODOS los procesos que existen en la fábrica
                todos_los_procesos = conexion.obtener_todos_los_tipos_proceso()
                
                for p in todos_los_procesos:
                    nombre_proceso = p[0]
                    if nombre_proceso in procesos_asignados:
                        self.lista_seleccionados.addItem(nombre_proceso)
                    else:
                        self.lista_disponibles.addItem(nombre_proceso)
                        
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los detalles: {error}")

    def procesar_actualizacion(self):
        codigo = self.combo_selector.currentText()
        if not codigo:
            return
            
        # 1. Recuperar los procesos del listbox derecho
        procesos_finales = []
        for i in range(self.lista_seleccionados.count()):
            procesos_finales.append(self.lista_seleccionados.item(i).text())
            
        # 2. Validación (manteniendo la misma coherencia que al cargar)
        if not procesos_finales:
            QMessageBox.warning(
                self, 
                "Faltan Procesos", 
                "¡Atención! Un ítem activo debe contar con al menos un proceso asignado en el listbox derecho."
            )
            return

        # 3. Recopilar datos generales
        datos = {
            "codigo_item": codigo,
            "color": self.input_color.text().strip() or None,
            "descripcion": self.input_descripcion.text().strip() or None,
            "peso": self.input_peso.value(),
            "tipo_item": self.combo_tipo.currentText(),
            "ancho": self.input_ancho.value(),
            "largo": self.input_largo.value(),
            "diametro": self.input_diametro.value(),
            "espesor": self.input_espesor.value(),
            "largo_tira_tubo": self.input_largo_tira.value(),
            "precio_materia_prima": self.input_precio_mp.value()
        }
        
        try:
            # 4. Guardar mediante la nueva transacción de actualización completa
            if conexion.actualizar_item_con_procesos(datos, procesos_finales):
                QMessageBox.information(self, "Éxito", "Ítem y su listado de procesos actualizados correctamente.")
                # Recargamos la información para confirmar los cambios visualmente
                self.cargar_datos_del_item(codigo)
        except Exception as error:
            QMessageBox.critical(self, "Error al actualizar", f"No se pudieron guardar las modificaciones: {error}")