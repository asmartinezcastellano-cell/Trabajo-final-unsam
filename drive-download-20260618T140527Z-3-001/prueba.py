from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QListWidget, QPushButton, QMessageBox)
import conexion

class VistaGuardarItemDosListas(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # ... Tus inputs normales de arriba (Código, Descripción, etc.) ...
        self.input_codigo = QLineEdit()
        layout.addWidget(QLabel("Código del Ítem:"))
        layout.addWidget(self.input_codigo)
        
        # --- NUEVA SECCIÓN: DUAL LISTBOX ---
        layout.addWidget(QLabel("<b>Asignación de Procesos (Obligatorio):</b>"))
        
        # Layout horizontal para contener las dos listas y los botones del medio
        dual_list_layout = QHBoxLayout()
        
        # 1. Lista Izquierda: Procesos Disponibles
        self.lista_disponibles = QListWidget()
        
        # 2. Layout Vertical para los botones del medio
        botones_medio_layout = QVBoxLayout()
        self.btn_agregar = QPushButton("→")
        self.btn_agregar.setStyleSheet("font-weight: bold; padding: 5px;")
        self.btn_quitar = QPushButton("←")
        self.btn_quitar.setStyleSheet("font-weight: bold; padding: 5px;")
        
        botones_medio_layout.addStretch()
        botones_medio_layout.addWidget(self.btn_agregar)
        botones_medio_layout.addWidget(self.btn_quitar)
        botones_medio_layout.addStretch()
        
        # 3. Lista Derecha: Procesos Seleccionados (Empieza vacía)
        self.lista_seleccionados = QListWidget()
        
        # Unimos todo en el layout horizontal
        dual_list_layout.addWidget(self.lista_disponibles)
        dual_list_layout.addLayout(botones_medio_layout)
        dual_list_layout.addWidget(self.lista_seleccionados)
        
        layout.addLayout(dual_list_layout)
        # ----------------------------------------------------
        
        # Botón de Guardar final
        self.boton_guardar = QPushButton("Guardar Ítem")
        self.boton_guardar.setStyleSheet("padding: 10px; font-weight: bold; background-color: #4CAF50; color: white;")
        layout.addWidget(self.boton_guardar)
        
        self.setLayout(layout)
        
        # --- CONEXIONES DE EVENTOS ---
        self.btn_agregar.clicked.connect(self.mover_a_seleccionados)
        self.btn_quitar.clicked.connect(self.mover_a_disponibles)
        # Doble click para que sea aún más rápido pasar de un lado al otro
        self.lista_disponibles.itemDoubleClicked.connect(self.mover_a_seleccionados)
        self.lista_seleccionados.itemDoubleClicked.connect(self.mover_a_disponibles)
        
        # Cargamos los procesos desde la BD
        self.cargar_procesos_iniciales()

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
        """Pasa el proceso seleccionado de la izquierda a la derecha"""
        item_actual = self.lista_disponibles.currentItem()
        if item_actual:
            # Lo sumamos a la derecha y lo borramos de la izquierda para que no se duplique
            self.lista_seleccionados.addItem(item_actual.text())
            self.lista_disponibles.takeItem(self.lista_disponibles.row(item_actual))

    def mover_a_disponibles(self):
        """Devuelve el proceso de la derecha a la izquierda (des-seleccionar)"""
        item_actual = self.lista_seleccionados.currentItem()
        if item_actual:
            self.lista_disponibles.addItem(item_actual.text())
            self.lista_seleccionados.takeItem(self.lista_seleccionados.row(item_actual))

    def procesar_guardado(self):
        """Valida que la lista de la derecha no esté vacía y guarda todo"""
        # 1. Recuperar todos los elementos que quedaron en la lista de seleccionados
        procesos_finales = []
        for i in range(self.lista_seleccionados.count()):
            procesos_finales.append(self.lista_seleccionados.item(i).text())
            
        # 2. VALIDACIÓN: Obligar a que tenga al menos uno
        if not procesos_finales:
            QMessageBox.warning(
                self, 
                "Faltan Procesos", 
                "¡Atención! Debes pasar a la lista de la derecha al menos un proceso para este ítem."
            )
            return # Frena el guardado
            
        # 3. Armar los datos del ítem (ejemplo)
        datos_item = {
            "codigo_item": self.input_codigo.text(),
            "color": "Negro", "descripcion": "Soporte Reforzado", "peso": 2.1,
            "tipo_item": "Perfil", "ancho": 5.0, "largo": 12.0, "diametro": 0.0,
            "espesor": 3.5, "largo_tira_tubo": 0.0, "precio_materia_prima": 800.0
        }
        
        try:
            # Llamamos a la función con transacción que ya armamos antes en conexion.py
            conexion.guardar_item_con_procesos(datos_item, procesos_finales)
            QMessageBox.information(self, "Éxito", "Ítem registrado con sus procesos correctamente.")
            self.cargar_procesos_iniciales() # Limpia y resetea las listas
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudo guardar en la BD: {error}")