from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QSpinBox, QDoubleSpinBox, 
                               QPushButton, QComboBox, QMessageBox, QScrollArea)

import conexion

# ============================================================================
# VISTA PARA CARGAR/CREAR NUEVOS ITEMS (PRODUCTOS)
# ============================================================================
# Esta clase define la interfaz para registrar nuevos productos/items en 
# la base de datos. Incluye campos técnicos detallados y validación de datos.
# ============================================================================

class VistaCargarItem(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz completa de carga de items.
    #
    # Estructura del formulario (con QScrollArea para desplazamiento):
    #
    #   IDENTIFICACIÓN:
    #   - Código de Item (*): Código único (máx 10 caracteres, obligatorio)
    #   - Tipo de Item: Selector desplegable de categorías
    #
    #   DESCRIPCIÓN:
    #   - Descripción: Texto descriptivo (máx 100 caracteres)
    #   - Color: Color del producto (máx 20 caracteres)
    #
    #   ESPECIFICACIONES TÉCNICAS (dos columnas):
    #   Columna izquierda:
    #     - Peso (kg)
    #     - Ancho (mm)
    #     - Largo (mm)
    #   Columna derecha:
    #     - Diámetro (mm)
    #     - Espesor (mm)
    #     - Largo Tira/Tubo (mm)
    #
    #   PRECIO:
    #   - Precio Materia Prima ($)
    #
    # El botón "Guardar Item en Base de Datos" ejecuta procesar_formulario()
    # ________________________________________________________________________
    
    def __init__(self):
        super().__init__()
        
        # Configuración del layout principal con scroll
        scroll_layout = QVBoxLayout()
        self.setLayout(scroll_layout)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_layout.addWidget(scroll)
        
        contenedor = QWidget()
        layout = QVBoxLayout(contenedor)
        scroll.setWidget(contenedor)
        
        # Título de la sección
        label_titulo = QLabel("Registrar Nuevo Item / Producto")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 15px;")
        layout.addWidget(label_titulo)

        # Campos del formulario
        layout.addWidget(QLabel("Código de Item (*):"))
        self.input_codigo = QLineEdit()
        self.input_codigo.setMaxLength(10)  # ¡Ahora sí funcionará!
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

       
        self.boton_guardar = QPushButton("Guardar Item en Base de Datos")
        self.boton_guardar.setStyleSheet("padding: 10px; font-weight: bold; background-color: #2b78e4; color: white; margin-top: 15px;")
        self.boton_guardar.clicked.connect(self.procesar_formulario)
        layout.addWidget(self.boton_guardar)
        
        layout.addStretch()

    # ________________________________________________________________________
    # cargar_tipos_items()
    # ________________________________________________________________________
    # Carga todas las categorías disponibles de tipos de items en el ComboBox.
    #
    # Operaciones:
    #   1. Obtiene todos los tipos de items registrados desde BD
    #   2. Agrega cada tipo al ComboBox de selección
    #   3. Si no hay tipos: muestra mensaje "No hay tipos de items disponibles"
    #
    # Se ejecuta automáticamente en __init__().
    # ________________________________________________________________________
    
    def cargar_tipos_items(self):
        """Busca los tipos de items para rellenar el ComboBox"""
        try:
            tipos = conexion.obtener_todos_los_tipos_item()
            if not tipos:
                self.combo_tipo.addItem("No hay tipos de items disponibles")
                return
            for tipo in tipos:
                tipo_item = tipo[0]
                self.combo_tipo.addItem(tipo_item)            
        except Exception as e:
            self.combo_tipo.addItem("Error al cargar tipos")
            print(f"Error cargando tipos de item: {e}")

    # ________________________________________________________________________
    # procesar_formulario()
    # ________________________________________________________________________
    # Valida y procesa todos los datos ingresados en el formulario de item.
    #
    # Validaciones realizadas:
    #   1. El campo 'Código de Item' no debe estar vacío (obligatorio)
    #
    # Flujo de ejecución:
    #   1. Obtiene y limpia el código de item
    #   2. Valida que el código no esté vacío
    #   3. Arma diccionario con TODOS los datos del item:
    #      - Identificación: código, tipo
    #      - Descripción: descripción, color
    #      - Técnicos: peso, ancho, largo, diámetro, espesor, largo_tira_tubo
    #      - Precio: precio_materia_prima
    #   4. Llama a conexion.guardar_item() para guardar en BD
    #   5. Si éxito: muestra mensaje y limpia formulario
    #   6. Si error: muestra mensaje de error
    #
    # Excepciones manejadas:
    #   - Si código_item ya existe (clave única)
    #   - Errores de validación de datos
    # ________________________________________________________________________
    def procesar_formulario(self):
        codigo = self.input_codigo.text().strip()
        tipo_seleccionado = self.combo_tipo.currentText()

        if not codigo:
            QMessageBox.warning(self, "Error de validación", "El campo 'Código de Item' es obligatorio.")
            return
        
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

        conexion.guardar_item(datos_item)
        self.limpiar_campos()
    
    # ________________________________________________________________________
    # limpiar_campos()
    # ________________________________________________________________________
    # Reinicia todos los campos del formulario a sus valores por defecto.
    #
    # Nota: Solo limpia los primeros 3 campos en el código actual.
    #       Podría extenderse para limpiar todos los campos.
    # ________________________________________________________________________
    #Limpiar campos del formulario después de guardar
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