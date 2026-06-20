from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTableWidget, QTableWidgetItem, QPushButton, 
                               QMessageBox, QScrollArea, QAbstractItemView, QHeaderView)
import conexion

class VistaListarProductos(QWidget):
    def __init__(self):
        super().__init__()        
        
        layout_principal = QVBoxLayout(self)
        
        label_titulo = QLabel("Listado y Consulta de Productos")
        label_titulo.setStyleSheet("font-size : 20px; font-weight:bold; margin-bottom: 10px; color: #2C3E50;")
        layout_principal.addWidget(label_titulo)
        
        # Botón para refrescar manualmente la información
        self.btn_actualizar = QPushButton("🔄 Actualizar Lista")
        self.btn_actualizar.setStyleSheet("padding: 6px; font-weight: bold; background-color: #7F8C8D; color: white; max-width: 150px;")
        self.btn_actualizar.clicked.connect(self.cargar_productos)
        layout_principal.addWidget(self.btn_actualizar)

        # --- TABLA MAESTRA: PRODUCTOS ---
        layout_principal.addWidget(QLabel("<b>Seleccione un producto para ver sus ítems componentes:</b>"))
        self.tabla_productos = QTableWidget(0, 4)
        self.tabla_productos.setHorizontalHeaderLabels(["Modelo", "Descripción", "Color", "Embalaje"])
        self.tabla_productos.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_productos.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabla_productos.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout_principal.addWidget(self.tabla_productos)

        # --- TABLA DETALLE: ÍTEMS DEL PRODUCTO SELECCIONADO ---
        layout_principal.addWidget(QLabel("<b>Componentes del Producto Seleccionado:</b>"))
        self.tabla_items = QTableWidget(0, 2)
        self.tabla_items.setHorizontalHeaderLabels(["Código de Ítem", "Cantidad Necesaria"])
        self.tabla_items.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabla_items.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla_items.setStyleSheet("QTableWidget { background-color: #F8F9F9; }")
        layout_principal.addWidget(self.tabla_items)

        # Conectar el evento de cambio de selección en la tabla de productos
        self.tabla_productos.itemSelectionChanged.connect(self.mostrar_items_del_producto)

        # Cargar datos por primera vez
        self.cargar_productos()

    def cargar_productos(self):
        """Trae los productos de la base de datos y los vuelca en la tabla maestra"""
        try:
            self.tabla_productos.setRowCount(0)
            self.tabla_items.setRowCount(0) # Limpiar el detalle también
            
            productos = conexion.obtener_todos_los_productos_completo()
            
            for fila_idx, prod in enumerate(productos):
                self.tabla_productos.insertRow(fila_idx)
                self.tabla_productos.setItem(fila_idx, 0, QTableWidgetItem(str(prod[0]))) # Modelo
                self.tabla_productos.setItem(fila_idx, 1, QTableWidgetItem(str(prod[1]) if prod[1] else "")) # Descripcion
                self.tabla_productos.setItem(fila_idx, 2, QTableWidgetItem(str(prod[2]) if prod[2] else "")) # Color
                self.tabla_productos.setItem(fila_idx, 3, QTableWidgetItem(str(prod[3]) if prod[3] else "Sin Embalaje")) # Embalaje
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los productos: {e}")

    def mostrar_items_del_producto(self):
        """Detecta qué producto está seleccionado y busca sus ítems asociados"""
        filas_seleccionadas = self.tabla_productos.selectedItems()
        if not filas_seleccionadas:
            return
            
        # El modelo está en la primera columna (columna 0) del elemento seleccionado
        fila_actual = self.tabla_productos.currentRow()
        modelo_seleccionado = self.tabla_productos.item(fila_actual, 0).text()
        
        try:
            self.tabla_items.setRowCount(0)
            # Reutilizamos la función de consulta que creamos para la ventana de modificar
            items_asociados = conexion.obtener_items_por_modelo_producto(modelo_seleccionado)
            
            if not items_asociados:
                # Si por algún motivo el producto quedó huérfano de ítems
                self.tabla_items.insertRow(0)
                self.tabla_items.setItem(0, 0, QTableWidgetItem("Sin ítems asociados"))
                self.tabla_items.setItem(0, 1, QTableWidgetItem("-"))
                return

            for fila_idx, (codigo_item, cantidad) in enumerate(items_asociados):
                self.tabla_items.insertRow(fila_idx)
                self.tabla_items.setItem(fila_idx, 0, QTableWidgetItem(str(codigo_item)))
                self.tabla_items.setItem(fila_idx, 1, QTableWidgetItem(str(cantidad)))
                
        except Exception as e:
            print(f"Error al cargar los ítems del producto: {e}")