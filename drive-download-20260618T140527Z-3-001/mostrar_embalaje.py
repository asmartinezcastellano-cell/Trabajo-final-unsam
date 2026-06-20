from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                             QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QHeaderView)
import conexion

# ============================================================================
# VISTA PARA MOSTRAR Y VISUALIZAR EMBALAJES
# ============================================================================
# Esta clase muestra todos los embalajes registrados en una tabla interactiva
# con opción para actualizar/refrescar los datos.
# ============================================================================

class VistaVerEmbalaje(QWidget):
    
    # ________________________________________________________________________
    # __init__()
    # ________________________________________________________________________
    # Inicializa la interfaz de visualización de embalajes.
    #
    # Componentes:
    #   - Título: "Inventario de Embalajes"
    #   - Tabla (QTableWidget):
    #     * Columnas: Tipo, Stock, Costo ($), Última Actualización
    #     * Se estira automáticamente para ocupar toda la ventana
    #   - Botón "Actualizar Tabla": Recarga datos de la BD
    #
    # Se llama a cargar_datos_en_tabla() automáticamente al inicializar.
    # ________________________________________________________________________
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()        
      
        titulo = QLabel("Inventario de Embalajes")
        titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px;")
        layout.addWidget(titulo)
        
       
        self.tabla = QTableWidget()
        
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["Tipo de Embalaje", "Stock", "Costo ($)", "Última Actualización"])
        
        #estira la tabla para que ocupe toda la ventana
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.tabla)
        
        # boton que carga o actualiza los cambios
        self.boton_refrescar = QPushButton("Actualizar Tabla")
        self.boton_refrescar.setStyleSheet("padding: 8px; font-weight: bold; background-color: #2ca02c; color: white;")
        self.boton_refrescar.clicked.connect(self.cargar_datos_en_tabla)
        layout.addWidget(self.boton_refrescar)
        
        self.setLayout(layout)
        
        
        self.cargar_datos_en_tabla()

    # ________________________________________________________________________
    # cargar_datos_en_tabla()
    # ________________________________________________________________________
    # Recupera todos los embalajes de la BD y los muestra en la tabla.
    #
    # Flujo de ejecución:
    #   1. Llama a conexion.obtener_todos_los_embalajes()
    #   2. Establece el número de filas según registros obtenidos
    #   3. Itera sobre cada registro y lo agrega a la tabla celda por celda
    #
    # La tabla se auto-actualiza mostrando la información más reciente.
    #
    # Excepciones:
    #   - Si hay error de conexión, muestra mensaje de error al usuario
    # ________________________________________________________________________
    def cargar_datos_en_tabla(self):
        try:
            # traigo los datos de bd
            registros = conexion.obtener_todos_los_embalajes()
            
            # cuenta las filas
            self.tabla.setRowCount(len(registros))
            
            # llena la tabla celda por celda
            for numero_fila, fila_datos in enumerate(registros):
                for numero_columna, valor in enumerate(fila_datos):
                    item = QTableWidgetItem(str(valor))
                    self.tabla.setItem(numero_fila, numero_columna, item)
                    
        except Exception as error:
            QMessageBox.critical(self, "Error al cargar datos", f"No se pudo leer la base de datos: {error}")