# SoriSound

## Resumen general

SoriSound es una aplicación de escritorio en Python que usa `PySide6` para la interfaz gráfica y `mysql.connector` para persistencia en una base de datos MySQL. La app centraliza operaciones CRUD sobre:

- Embalajes
- Tipos de ítems
- Ítems / productos intermedios
- Procesos
- Productos finales

La ventana principal funciona como un hub de navegación que muestra diferentes pantallas según la opción seleccionada en el menú.

## Arquitectura principal

### `Sorisound/ventana_principal.py`

Este archivo define la clase principal:

- `class VentanaPrincipal(QMainWindow)`

`VentanaPrincipal` hereda de `QMainWindow`, lo que le permite tener:

- una barra de menú (`menuBar()`)
- un área de contenido central (`setCentralWidget(...)`)
- un ciclo de eventos propio de Qt

Dentro de su constructor, la clase:

1. llama a `super().__init__()` para inicializar el `QMainWindow`
2. configura el título y tamaño de la ventana
3. crea un `QStackedWidget` llamado `self.contenedor_pantallas`
4. agrega todas las vistas de la aplicación al `QStackedWidget`
5. crea el menú con acciones que cambian la vista actual

### `QStackedWidget` y la herencia de vistas

La navegación no usa ventanas separadas, sino una sola ventana principal con un contenedor de pantallas:

- `self.contenedor_pantallas = QStackedWidget()`

Cada pantalla es un widget propio que hereda de `QWidget`, por ejemplo:

- `cargar_embalaje.VistaCargarEmbalaje(QWidget)`
- `mostrar_embalaje.VistaVerEmbalaje(QWidget)`
- `actualizar_embalaje.VistaActualizarEmbalaje(QWidget)`

Estas clases son compatibles con `QStackedWidget`, porque `QStackedWidget` recibe widgets de Qt y muestra solo uno a la vez.

## Flujo de navegación

La ventana principal agrega las vistas en un orden fijo. Cada opción del menú hace lo siguiente:

- crea un `QAction`
- conecta su señal `triggered` a un `lambda`
- el `lambda` cambia el índice actual de `self.contenedor_pantallas`

Ejemplo:

```python
accion_cargar_embalaje.triggered.connect(lambda: self.contenedor_pantallas.setCurrentIndex(0))
```

Cada índice está asociado a una pantalla fija. Por eso, el orden de `addWidget(...)` en el constructor es importante.

## Estructura de módulos y pantallas

La carpeta `Sorisound/` organiza las vistas por funcionalidad. Cada grupo maneja una parte del modelo:

- Embalaje:
  - `cargar_embalaje.py`
  - `mostrar_embalaje.py`
  - `actualizar_embalaje.py`
  - `eliminar_embalaje.py`

- Tipo de ítem:
  - `cargar_tipo_item.py`
  - `mostrar_tipo_item.py`
  - `eliminar_tipo_item.py`

- Ítem:
  - `cargar_item.py`
  - `mostrar_items.py`
  - `actualizar_item.py`
  - `eliminar_item.py`

- Proceso:
  - `cargar_proceso.py`
  - `mostrar_procesos.py`
  - `actualizar_proceso.py`
  - `eliminar_proceso.py`

- Producto:
  - `cargar_producto.py`
  - `mostrar_producto.py`
  - `actualizar_producto.py`
  - `eliminar_producto.py`

## Módulo de datos

### `Sorisound/conexion.py`

Este módulo centraliza la conexión a la base de datos y las operaciones CRUD. Sus responsabilidades principales son:

- abrir y cerrar la conexión con `obtener_conexion()`
- ejecutar consultas `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- devolver resultados para las vistas
- manejar excepciones de MySQL

Ejemplos de funciones:

- `guardar_embalaje(datos)`
- `obtener_todos_los_embalajes()`
- `actualizar_embalaje(datos)`
- `eliminar_embalaje(tipo_embalaje)`
- `guardar_tipo_item(nombre_tipo)`
- `obtener_todos_los_codigos_item()`
- `guardar_producto_con_items(datos_producto, items_finales)`

## Cómo funciona cada pantalla

### Vistas de carga

Las pantallas de carga (`cargar_*.py`) muestran formularios con campos Qt como:

- `QLineEdit` para texto
- `QSpinBox` / `QDoubleSpinBox` para valores numéricos
- `QComboBox` para elegir opciones relacionadas
- `QListWidget` para listas de selección

Estas vistas validan los datos del formulario y llaman a funciones de `conexion.py` para insertar registros.

### Vistas de consulta

Las pantallas de consulta (`mostrar_*.py`) usan tablas `QTableWidget` para mostrar los datos obtenidos de la base.

- cargan la información al inicializarse
- permiten refrescar con un botón
- no editan datos directamente, solo muestran resultados

### Vistas de actualización y eliminación

Las pantallas de actualización (`actualizar_*.py`) y eliminación (`eliminar_*.py`) combinan:

- `QComboBox` para elegir el registro a modificar/eliminar
- carga de datos actuales desde la BD
- edición y guardado de cambios
- confirmación y mensajes de error con `QMessageBox`

## Herencia y clase padre

En esta aplicación, la herencia se usa de la siguiente forma:

- `VentanaPrincipal` hereda de `QMainWindow`
- Cada vista principal hereda de `QWidget`

No hay una clase base propia del proyecto que actúe como padre común entre todas las vistas. En cambio, la herencia se apoya en las clases de Qt:

- `QMainWindow` aporta estructura de ventana principal y menú
- `QWidget` aporta capacidad de contener layouts y widgets

Cada clase de vista llama a `super().__init__()` en su constructor para inicializar su clase padre de Qt.

## Ejecución

Para ejecutar la aplicación desde el directorio raíz del proyecto:

```bash
python Sorisound/ventana_principal.py
```

Requisitos:

- Python 3.x
- PySide6
- mysql-connector-python
- Una base de datos MySQL configurada con los datos correctos en `Sorisound/conexion.py`

## Notas importantes

- El archivo `Sorisound/conexion.py` usa credenciales y base de datos: `host=localhost`, `user=los_pibes`, `password=SanMartin1023`, `database=sorisound`.
- Si la base de datos no existe o las tablas no están creadas, varias vistas fallarán al intentar leer o escribir.
- El orden en que se agregan las pantallas al `QStackedWidget` debe mantenerse si se conserva la lógica de índices del menú.

## Extender la aplicación

Para agregar una nueva pantalla, el patrón es:

1. crear un módulo `Sorisound/mi_nueva_vista.py`
2. definir `class VistaMiNuevaPantalla(QWidget)`
3. implementar el layout y la lógica de datos
4. importar el módulo en `Sorisound/ventana_principal.py`
5. instanciar la vista y `addWidget(...)` en el constructor
6. agregar una acción de menú que llame a `setCurrentIndex(...)`

Esto mantiene la arquitectura consistente con el diseño actual.
