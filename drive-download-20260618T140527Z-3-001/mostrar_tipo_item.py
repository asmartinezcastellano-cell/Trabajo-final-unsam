from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView
import conexion

# ============================================================================
# VISTA PARA MOSTRAR TIPOS DE ITEMS REGISTRADOS
# ============================================================================
# Esta clase muestra todas las categor\u00edas de tipos de items en una tabla
# interactiva con opci\u00f3n para actualizar los datos.
# ============================================================================

class VistaMostrarTipoItem(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de visualizaci\u00f3n de tipos de items.
    #
    # Componentes:
    #   - T\u00edtulo: "Tipos de Ítems Registrados"
    #   - Tabla (QTableWidget):
    #     * Columna \u00fanica: Tipo de Ítem
    #     * Se estira para ocupar toda la ventana
    #   - Bot\u00f3n "Actualizar Lista": Recarga datos de BD
    #
    # Se llama a cargar_datos_en_tabla() autom\u00e1ticamente al inicializar.
    # ________________________________________________________________________
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        titulo = QLabel("Tipos de Ítems Registrados")
        titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(1)
        self.tabla.setHorizontalHeaderLabels(["Tipo de Ítem"])
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tabla)
        
        self.boton_refrescar = QPushButton("Actualizar Lista")
        self.boton_refrescar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2ca02c; color: white;")
        self.boton_refrescar.clicked.connect(self.cargar_datos_en_tabla)
        layout.addWidget(self.boton_refrescar)
        
        self.setLayout(layout)
        self.cargar_datos_en_tabla()
        
        
    # ________________________________________________________________________
    # cargar_datos_en_tabla()
    # ________________________________________________________________________
    # Recupera todos los tipos de items de la BD y los muestra en la tabla.
    #
    # Flujo de ejecuci\u00f3n:
    #   1. Llama a conexion.obtener_todos_los_tipos_item()
    #   2. Establece el n\u00famero de filas seg\u00fan registros obtenidos
    #   3. Itera sobre cada registro y lo agrega a la tabla
    #
    # Se ejecuta autom\u00e1ticamente en __init__() y cuando el usuario
    # hace clic en el bot\u00f3n "Actualizar Lista".
    # ________________________________________________________________________
    def cargar_datos_en_tabla(self):
        try:
            registros = conexion.obtener_todos_los_tipos_item()
            self.tabla.setRowCount(len(registros))
            
            for numero_fila, fila_datos in enumerate(registros):
                item = QTableWidgetItem(str(fila_datos[0]))
                self.tabla.setItem(numero_fila, 0, item)
        except Exception as error:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los datos: {error}")