"""
MÓDULO: conexion.py - Gestión de conexiones y operaciones CRUD con MySQL
Sistema SoriSound: Embalajes, Items, Procesos, Productos
"""

import mysql.connector

# Establece conexión a la base de datos MySQL del sistema
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="los_pibes",
        password="SanMartin1023",
        database="sorisound"
    )

# ==================== EMBALAJES ==================== 

# Inserta nuevo embalaje en la BD (tipo, stock, costo, fecha)
def guardar_embalaje(datos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            INSERT INTO embalaje (tipo, stock, costo, fecha_ultima_actualizacion) 
            VALUES (%s, %s, %s, %s)
        """
        valores = (
            datos['tipo'], 
            datos['stock'], 
            datos['costo'], 
            datos['fecha']
        )
        cursor.execute(query, valores)
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene lista de todos los embalajes registrados
def obtener_todos_los_embalajes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    try:
        query = "SELECT tipo, stock, costo, fecha_ultima_actualizacion FROM embalaje"
        cursor.execute(query)
        return cursor.fetchall() 
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Busca embalaje específico por tipo, retorna (stock, costo)
def obtener_embalaje_por_tipo(tipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT stock, costo FROM embalaje WHERE tipo = %s"
        cursor.execute(query, (tipo,))
        return cursor.fetchone()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Actualiza stock, costo y fecha de un embalaje existente
def actualizar_embalaje(datos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            UPDATE embalaje 
            SET stock = %s, costo = %s, fecha_ultima_actualizacion = %s 
            WHERE tipo = %s
        """
        valores = (datos['stock'], datos['costo'], datos['fecha'], datos['tipo'])
        cursor.execute(query, valores)
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Elimina un embalaje de la BD (verifica integridad referencial)
def eliminar_embalaje(tipo_embalaje):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            DELETE FROM embalaje
            WHERE tipo = %s
        """
        cursor.execute(query, (tipo_embalaje,))
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# ==================== TIPOS DE ITEM ====================

# Inserta nuevo tipo de ítem en la BD
def guardar_tipo_item(nombre_tipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "INSERT INTO tipo_item(tipo) VALUES (%s)"
        cursor.execute(query, (nombre_tipo,))
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene lista de todos los tipos de ítem registrados
def obtener_todos_los_tipos_item():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT tipo FROM tipo_item"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Elimina un tipo de ítem de la BD
def borrar_tipo_item(tipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """DELETE FROM tipo_item WHERE tipo = %s """
        cursor.execute(query,(tipo,))
        conexion.commit()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()


# ==================== ITEMS ====================

# Inserta nuevo ítem con especificaciones técnicas y dimensiones
def guardar_item(datos_item):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            INSERT INTO item (
                codigo_item, color, descripcion, peso, tipo_item, 
                ancho, largo, diametro, espesor, largo_tira_tubo, precio_materia_prima
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        valores = (
            datos_item["codigo_item"],
            datos_item["color"],
            datos_item["descripcion"],
            datos_item["peso"],
            datos_item["tipo_item"],
            datos_item["ancho"],
            datos_item["largo"],
            datos_item["diametro"],
            datos_item["espesor"],
            datos_item["largo_tira_tubo"],
            datos_item["precio_materia_prima"]
        )
        
        
        cursor.execute(query, valores)
        conexion.commit()
        return True
        
    except mysql.connector.Error as error:
        conexion.rollback()
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene lista de todos los códigos de ítems
def obtener_todos_los_codigos_item():
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_item FROM item")
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

# Busca un ítem específico por código
def obtener_item_por_codigo(codigo):
    conn = obtener_conexion()
    cursor = conn.cursor()
    query = "SELECT codigo_item, color, descripcion, peso, tipo_item, ancho, largo, diametro, espesor, largo_tira_tubo, precio_materia_prima FROM item WHERE codigo_item = %s"
    cursor.execute(query, (codigo,))
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    return res

# Actualiza datos de un ítem (color, descripción, especificaciones, etc.)
def actualizar_item(d):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        query = """
            UPDATE item SET 
            color=%s, descripcion=%s, peso=%s, tipo_item=%s, ancho=%s, 
            largo=%s, diametro=%s, espesor=%s, largo_tira_tubo=%s, precio_materia_prima=%s 
            WHERE codigo_item=%s
        """
        valores = (d["color"], d["descripcion"], d["peso"], d["tipo_item"], d["ancho"], 
                   d["largo"], d["diametro"], d["espesor"], d["largo_tira_tubo"], 
                   d["precio_materia_prima"], d["codigo_item"])
        cursor.execute(query, valores)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        cursor.close()
        conn.close()


# Obtiene lista completa de ítems con todos sus datos
def obtener_todos_los_items_completo():
    # Trae todas las filas y columnas de la tabla item
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        query = """
            SELECT codigo_item, color, descripcion, peso, tipo_item, 
                   ancho, largo, diametro, espesor, largo_tira_tubo, precio_materia_prima 
            FROM item
        """
        cursor.execute(query)
        resultado = cursor.fetchall()
        return resultado
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conn.close()
        

# Elimina un ítem de la tabla por su código
def eliminar_item_por_codigo(codigo):
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        query = "DELETE FROM item WHERE codigo_item = %s"
        cursor.execute(query, (codigo,))
        conn.commit()
        return True
    except mysql.connector.Error as error:
        conn.rollback() 
        raise error
    finally:
        cursor.close()
        conn.close()


# ==================== PROCESOS ====================

# Inserta nuevo proceso en la BD (tipo, costo, fecha)
def guardar_proceso(datos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()    
    try:
        query = """
            INSERT INTO proceso (tipo_proceso, costo, fecha) 
            VALUES (%s, %s, %s)
        """
        valores = (
            datos['tipo_proceso'], 
            datos['costo'], 
            datos['fecha']
        )        
        cursor.execute(query, valores)
        conexion.commit()
        return True
        
    except mysql.connector.Error as error:        
        raise error        
    finally:
        cursor.close()
        conexion.close()

# Obtiene lista de todos los tipos de procesos únicos
def obtener_todos_los_tipos_proceso():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT DISTINCT tipo_proceso FROM proceso"
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene costo del proceso más reciente de un tipo específico
def obtener_proceso_por_tipo(tipo_proceso):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            SELECT costo 
            FROM proceso 
            WHERE tipo_proceso = %s 
            ORDER BY fecha DESC 
            LIMIT 1
        """
        cursor.execute(query, (tipo_proceso,))
        return cursor.fetchone() # Devuelve una tupla (costo,) o None
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Actualiza costo y fecha de un proceso existente
def actualizar_proceso(datos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            UPDATE proceso 
            SET costo = %s, fecha = %s 
            WHERE tipo_proceso = %s
        """
        valores = (datos['costo'], datos['fecha'], datos['tipo_proceso'])
        cursor.execute(query, valores)
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()


# Obtiene lista completa de procesos para visualización
def obtener_todos_los_procesos_completo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Trae tipo, costo y fecha ordenados descendentemente
        query = "SELECT tipo_proceso, costo, fecha FROM proceso ORDER BY fecha DESC"
        cursor.execute(query)
        return cursor.fetchall() 
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()


# Elimina todos los registros de un tipo de proceso
def eliminar_proceso_por_tipo(tipo_proceso):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = """
            DELETE FROM proceso
            WHERE tipo_proceso = %s
        """
        cursor.execute(query, (tipo_proceso,))
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        conexion.rollback()
        raise error
    finally:
        cursor.close()
        conexion.close()


# Inserta ítem y sus procesos asociados en transacción única
def guardar_item_con_procesos(datos_item, lista_procesos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        # Inicia transacción explícita
        conexion.start_transaction()
        
        # Inserta el ítem
        query_item = """
            INSERT INTO item (
                codigo_item, color, descripcion, peso, tipo_item, 
                ancho, largo, diametro, espesor, largo_tira_tubo, precio_materia_prima
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores_item = (
            datos_item["codigo_item"], datos_item["color"], datos_item["descripcion"],
            datos_item["peso"], datos_item["tipo_item"], datos_item["ancho"],
            datos_item["largo"], datos_item["diametro"], datos_item["espesor"],
            datos_item["largo_tira_tubo"], datos_item["precio_materia_prima"]
        )
        cursor.execute(query_item, valores_item)
        
        # Inserta las relaciones en item_proceso
        query_proceso = "INSERT INTO item_proceso (codigo_item, tipo_proceso) VALUES (%s, %s)"
        for proceso in lista_procesos:
            cursor.execute(query_proceso, (datos_item["codigo_item"], proceso))
            
        # 4. Si todo salió bien, confirmamos en la BD
        conexion.commit()
        return True
        
    except mysql.connector.Error as error:
        conexion.rollback() # Si falló un proceso o el ítem, se deshace TODO
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene lista de procesos asociados a un ítem
def obtener_procesos_por_codigo_item(codigo_item):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT tipo_proceso FROM item_proceso WHERE codigo_item = %s"
        cursor.execute(query, (codigo_item,))
        # Convertimos la lista de tuplas [(p1,), (p2,)] en una lista limpia de textos [p1, p2]
        return [fila[0] for fila in cursor.fetchall()]
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Actualiza ítem y sus procesos asociados en transacción
def actualizar_item_con_procesos(datos_item, lista_procesos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        conexion.start_transaction()
        
        # Actualiza los campos generales de la tabla item
        query_update_item = """
            UPDATE item SET 
                color=%s, descripcion=%s, peso=%s, tipo_item=%s, ancho=%s, 
                largo=%s, diametro=%s, espesor=%s, largo_tira_tubo=%s, precio_materia_prima=%s 
            WHERE codigo_item=%s
        """
        valores_item = (
            datos_item["color"], datos_item["descripcion"], datos_item["peso"], 
            datos_item["tipo_item"], datos_item["ancho"], datos_item["largo"], 
            datos_item["diametro"], datos_item["espesor"], datos_item["largo_tira_tubo"], 
            datos_item["precio_materia_prima"], datos_item["codigo_item"]
        )
        cursor.execute(query_update_item, valores_item)
        
        # Elimina asignaciones anteriores de procesos para este ítem
        query_delete_procesos = "DELETE FROM item_proceso WHERE codigo_item = %s"
        cursor.execute(query_delete_procesos, (datos_item["codigo_item"],))
        
        # Inserta nuevo listado de procesos seleccionados
        query_insert_proceso = "INSERT INTO item_proceso (codigo_item, tipo_proceso) VALUES (%s, %s)"
        for proceso in lista_procesos:
            cursor.execute(query_insert_proceso, (datos_item["codigo_item"], proceso))
            
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        conexion.rollback()
        raise error
    finally:
        cursor.close()
        conexion.close()


# ==================== PRODUCTOS ====================

# Obtiene nombres de embalajes para el ComboBox
def obtener_todos_los_embalajes_combo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT tipo FROM embalaje")
        return cursor.fetchall()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Inserta producto e ítems asociados con cantidades en transacción
def guardar_producto_con_items(datos_producto, lista_items):
    # lista_items: [{"codigo_item": "...", "cantidad": 4}, ...]
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        conexion.start_transaction()
        
        # Inserta el Producto
        query_producto = """
            INSERT INTO producto (modelo, descripcion, color, embalaje) 
            VALUES (%s, %s, %s, %s)
        """
        valores_producto = (
            datos_producto["modelo"],
            datos_producto["descripcion"],
            datos_producto["color"],
            datos_producto["embalaje"]
        )
        cursor.execute(query_producto, valores_producto)
        
        # 2. Insertar las relaciones en producto_item con su cantidad
        query_item = """
            INSERT INTO producto_item (modelo, codigo_item, cantidad) 
            VALUES (%s, %s, %s)
        """
        for item in lista_items:
            cursor.execute(query_item, (datos_producto["modelo"], item["codigo_item"], item["cantidad"]))
            
        conexion.commit()
        return True
        
    except mysql.connector.Error as error:
        conexion.rollback()
        raise error
    finally:
        cursor.close()
        conexion.close()



# Obtiene lista de todos los modelos de productos
def obtener_todos_los_modelos_producto():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT modelo FROM producto")
        return cursor.fetchall()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene datos básicos de un producto específico
def obtener_producto_por_modelo(modelo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT modelo, descripcion, color, embalaje FROM producto WHERE modelo = %s"
        cursor.execute(query, (modelo,))
        return cursor.fetchone()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene ítems asociados a un producto con sus cantidades
def obtener_items_por_modelo_producto(modelo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT codigo_item, cantidad FROM producto_item WHERE modelo = %s"
        cursor.execute(query, (modelo,))
        return cursor.fetchall()
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()

# Actualiza producto e ítems asociados en transacción
def actualizar_producto_con_items(datos_producto, lista_items):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        conexion.start_transaction()
        
        # Actualiza datos de la tabla producto
        query_update = """
            UPDATE producto 
            SET descripcion = %s, color = %s, embalaje = %s 
            WHERE modelo = %s
        """
        valores_prod = (
            datos_producto["descripcion"],
            datos_producto["color"],
            datos_producto["embalaje"],
            datos_producto["modelo"]
        )
        cursor.execute(query_update, valores_prod)
        
        # Elimina relaciones anteriores en producto_item
        query_delete = "DELETE FROM producto_item WHERE modelo = %s"
        cursor.execute(query_delete, (datos_producto["modelo"],))
        
        # Inserta nuevo listado de ítems con sus cantidades
        query_insert = "INSERT INTO producto_item (modelo, codigo_item, cantidad) VALUES (%s, %s, %s)"
        for item in lista_items:
            cursor.execute(query_insert, (datos_producto["modelo"], item["codigo_item"], item["cantidad"]))
            
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        conexion.rollback()
        raise error
    finally:
        cursor.close()
        conexion.close()

# Obtiene lista completa de productos para visualización
def obtener_todos_los_productos_completo():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        query = "SELECT modelo, descripcion, color, embalaje FROM producto ORDER BY modelo"
        cursor.execute(query)
        return cursor.fetchall() 
    except mysql.connector.Error as error:
        raise error
    finally:
        cursor.close()
        conexion.close()


# Elimina producto y sus ítems asociados en transacción
def eliminar_producto_por_modelo(modelo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        conexion.start_transaction()
        
        # Elimina relaciones de ítems componentes
        query_items = "DELETE FROM producto_item WHERE modelo = %s"
        cursor.execute(query_items, (modelo,))
        
        # Elimina el producto maestro
        query_producto = "DELETE FROM producto WHERE modelo = %s"
        cursor.execute(query_producto, (modelo,))
        
        conexion.commit()
        return True
    except mysql.connector.Error as error:
        conexion.rollback()
        raise error
    finally:
        cursor.close()
        conexion.close()