from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QDoubleSpinBox, QPushButton, 
                               QComboBox, QMessageBox, QScrollArea, QFrame)
import conexion

# ============================================================================
# VISTA PARA ACTUALIZAR ITEMS EXISTENTES
# ============================================================================
# Esta clase permite modificar todos los datos de un item ya registrado.
# Incluye un selector de items, validación y actualización en la BD.
# ============================================================================

class VistaModificarItem(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz completa de edición/actualización de items.
    #
    # Estructura:
    #   PARTE SUPERIOR (Marco de búsqueda):
    #   - Selector de Código: ComboBox para elegir qué item editar
    #   - Al cambiar la selección, se cargan automáticamente sus datos
    #
    #   FORMULARIO (Con scroll para muchos campos):
    #   - Tipo de Item: ComboBox de categorías
    #   - Descripción, Color
    #   - Especificaciones: Peso, Ancho, Largo, Diámetro, Espesor, Largo Tira
    #   - Precio Materia Prima
    #   - Botón "Actualizar Datos en Base de Datos"
    # ________________________________________________________________________
    def __init__(self):
        super().__init__()
        
        layout_principal = QVBoxLayout(self)
        
        #parte superior de la ventana para que aparezca en un cuadradito
        frame_busqueda = QFrame()
        frame_busqueda.setFrameShape(QFrame.StyledPanel)
        layout_busqueda = QVBoxLayout(frame_busqueda)
        
        layout_busqueda.addWidget(QLabel("<b>Seleccione el Código del Item a modificar:</b>"))
        self.combo_selector = QComboBox()       
        self.combo_selector.currentTextChanged.connect(self.cargar_datos_del_item)
        layout_busqueda.addWidget(self.combo_selector)
        
        layout_principal.addWidget(frame_busqueda)

        
        #cuando usas scroll no se agrega directamente en el layout primero hay
        #que agregarlo en un contenedor

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

        # creo el layout horizontan y luego dos verticales que se los agrego

        grid_dim = QHBoxLayout()
        col_izq = QVBoxLayout()
        self.input_peso = QDoubleSpinBox(); self.input_peso.setRange(0, 99999)
        col_izq.addWidget(QLabel("Peso:")); col_izq.addWidget(self.input_peso)
        self.input_ancho = QDoubleSpinBox(); self.input_ancho.setRange(0, 99999)
        col_izq.addWidget(QLabel("Ancho:")); col_izq.addWidget(self.input_ancho)
        self.input_largo = QDoubleSpinBox(); self.input_largo.setRange(0, 99999)
        col_izq.addWidget(QLabel("Largo:")); col_izq.addWidget(self.input_largo)

        col_der = QVBoxLayout()
        self.input_diametro = QDoubleSpinBox(); self.input_diametro.setRange(0, 99999)
        col_der.addWidget(QLabel("Diámetro:")); col_der.addWidget(self.input_diametro)
        self.input_espesor = QDoubleSpinBox(); self.input_espesor.setRange(0, 99999)
        col_der.addWidget(QLabel("Espesor:")); col_der.addWidget(self.input_espesor)
        self.input_largo_tira = QDoubleSpinBox(); self.input_largo_tira.setRange(0, 99999)
        col_der.addWidget(QLabel("Largo Tira:")); col_der.addWidget(self.input_largo_tira)

        grid_dim.addLayout(col_izq)
        grid_dim.addLayout(col_der)
        self.layout_form.addLayout(grid_dim)

        self.layout_form.addWidget(QLabel("Precio Materia Prima ($):"))
        self.input_precio_mp = QDoubleSpinBox()
        self.input_precio_mp.setRange(0, 9999999)
        self.layout_form.addWidget(self.input_precio_mp)

        
        self.boton_actualizar = QPushButton("Actualizar Datos en Base de Datos")
        self.boton_actualizar.setStyleSheet("padding: 10px; background-color: #f39c12; color: white; font-weight: bold;")
        self.boton_actualizar.clicked.connect(self.procesar_actualizacion)
        self.layout_form.addWidget(self.boton_actualizar)
        
        self.layout_form.addStretch()

    # ________________________________________________________________________
    # refrescar_selectores()
    # ________________________________________________________________________
    # Carga todos los códigos de items disponibles en el ComboBox de selección.
    #
    # Se ejecuta automáticamente cuando se navega a esta pantalla desde el menú.
    # ________________________________________________________________________
    def refrescar_selectores(self):
        # Actualiza los datos del combo box
        codigos = conexion.obtener_todos_los_codigos_item()
        for c in codigos:
            self.combo_selector.addItem(c[0])

    # ________________________________________________________________________
    # cargar_tipos_en_combo()
    # ________________________________________________________________________
    # Carga todas las categorías de tipos disponibles en el ComboBox de tipo.
    #
    # Se ejecuta en __init__() para llenar el selector de tipos.
    # ________________________________________________________________________
    def cargar_tipos_en_combo(self):
        tipos = conexion.obtener_todos_los_tipos_item()
        for t in tipos:
            self.combo_tipo.addItem(t[0])

    # ________________________________________________________________________
    # cargar_datos_del_item(codigo)
    # ________________________________________________________________________
    # Obtiene los datos de un item específico y los carga en los campos
    # del formulario para su edición.
    #
    # Parámetros:
    #   - codigo (string): Código del item a cargar
    #
    # Flujo:
    #   1. Valida que el código no sea vacío
    #   2. Busca el item en BD
    #   3. Si existe: Llena todos los campos con sus datos
    #   4. Busca el índice del tipo en el ComboBox y lo selecciona
    #
    # Se ejecuta automáticamente cuando cambia la selección del combo de códigos.
    # ________________________________________________________________________
    def cargar_datos_del_item(self, codigo):
        # Setea los campos del formulario
        if not codigo: return
        
        item = conexion.obtener_item_por_codigo(codigo)
        if item:
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

    # ________________________________________________________________________
    # procesar_actualizacion()
    # ________________________________________________________________________
    # Valida y envía todos los cambios del item a la base de datos.
    #
    # Flujo de ejecución:
    #   1. Obtiene el código del item seleccionado
    #   2. Arma diccionario con TODOS los datos modificados
    #   3. Envía los cambios a BD mediante conexion.actualizar_item()
    #   4. Muestra mensaje de éxito si se actualizó correctamente
    # ________________________________________________________________________
    def procesar_actualizacion(self):
        codigo = self.combo_selector.currentText()
        datos = {
            "codigo_item": codigo,
            "color": self.input_color.text(),
            "descripcion": self.input_descripcion.text(),
            "peso": self.input_peso.value(),
            "tipo_item": self.combo_tipo.currentText(),
            "ancho": self.input_ancho.value(),
            "largo": self.input_largo.value(),
            "diametro": self.input_diametro.value(),
            "espesor": self.input_espesor.value(),
            "largo_tira_tubo": self.input_largo_tira.value(),
            "precio_materia_prima": self.input_precio_mp.value()
        }
        
        if conexion.actualizar_item(datos):
            QMessageBox.information(self, "Éxito", "Ítem actualizado correctamente.")