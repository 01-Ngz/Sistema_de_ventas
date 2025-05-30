# Funciones para productos, gestiona productos.
#Funcionalidades:Agregar, editar, eliminar, listar, buscar producto
# productos.py


DB_PATH = 'gaseosas_distribucion.db'

def conectar():
    return sqlite3.connect(DB_PATH)

def agregar_producto():
    conn = conectar()
    cursor = conn.cursor()
    try:
        nombre = input("Nombre del producto: ").strip()
        categoria = input("Categoría: ").strip()
        marca = input("Marca: ").strip()
        presentacion = input("Presentación: ").strip()
        proveedor = input("Proveedor: ").strip()
        precio_compra = float(input("Precio de compra: "))
        precio_venta = float(input("Precio de venta: "))
        stock_actual = int(input("Stock actual: "))
        stock_minimo = input("Stock mínimo (opcional, deja vacío para 0): ").strip()
        stock_minimo = int(stock_minimo) if stock_minimo else 0

        cursor.execute('''
            INSERT INTO productos (
                nombre, categoria, marca, presentacion, proveedor,
                precio_compra, precio_venta, stock_actual, stock_minimo
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, categoria, marca, presentacion, proveedor,
              precio_compra, precio_venta, stock_actual, stock_minimo))

        conn.commit()
        print("✅ Producto agregado correctamente.")
    except ValueError:
        print("❌ Error: Ingresa valores numéricos válidos para precios y stock.")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
    finally:
        conn.close()

def listar_productos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, categoria, marca, stock_actual, precio_venta FROM productos ORDER BY nombre")
    productos = cursor.fetchall()
    print("\n== Lista de productos ==")
    if productos:
        for p in productos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Categoría: {p[2]} | Marca: {p[3]} | Stock: {p[4]} | Precio venta: ${p[5]:.2f}")
    else:
        print("No hay productos registrados.")
    conn.close()

def buscar_producto_por_id():
    producto_id = input("Ingrese el ID del producto: ")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    p = cursor.fetchone()
    if p:
        print("\n== Detalles del producto ==")
        print(f"ID: {p[0]}")
        print(f"Nombre: {p[1]}")
        print(f"Categoría: {p[2]}")
        print(f"Marca: {p[3]}")
        print(f"Presentación: {p[4]}")
        print(f"Proveedor: {p[5]}")
        print(f"Precio compra: {p[6]:.2f}")
        print(f"Precio venta: {p[7]:.2f}")
        print(f"Stock actual: {p[8]}")
        print(f"Stock mínimo: {p[9]}")
    else:
        print("❌ Producto no encontrado.")
    conn.close()

def buscar_por_nombre():
    conn = conectar()
    cursor = conn.cursor()
    nombre = input("Buscar por nombre (parcial): ").strip()
    cursor.execute("SELECT id, nombre, stock_actual FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    productos = cursor.fetchall()
    if productos:
        print("\n== Resultados de búsqueda ==")
        for p in productos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Stock: {p[2]}")
    else:
        print("❌ No se encontraron productos con ese nombre.")
    conn.close()

def editar_producto():
    conn = conectar()
    cursor = conn.cursor()
    try:
        producto_id = int(input("ID del producto a editar: "))
    except ValueError:
        print("❌ ID inválido.")
        conn.close()
        return

    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    p = cursor.fetchone()
    if not p:
        print("❌ Producto no encontrado.")
        conn.close()
        return

    print("Deja en blanco si no deseas cambiar un campo.\n")
    nuevo_nombre = input(f"Nuevo nombre [{p[1]}]: ").strip() or p[1]
    nueva_categoria = input(f"Nueva categoría [{p[2]}]: ").strip() or p[2]
    nueva_marca = input(f"Nueva marca [{p[3]}]: ").strip() or p[3]
    nueva_presentacion = input(f"Nueva presentación [{p[4]}]: ").strip() or p[4]
    nuevo_proveedor = input(f"Nuevo proveedor [{p[5]}]: ").strip() or p[5]

    def pedir_float(prompt, valor_actual):
        entrada = input(prompt)
        if entrada.strip() == '':
            return valor_actual
        try:
            return float(entrada)
        except ValueError:
            print("Valor inválido, se mantiene el actual.")
            return valor_actual

    def pedir_int(prompt, valor_actual):
        entrada = input(prompt)
        if entrada.strip() == '':
            return valor_actual
        try:
            return int(entrada)
        except ValueError:
            print("Valor inválido, se mantiene el actual.")
            return valor_actual

    nuevo_precio_compra = pedir_float(f"Nuevo precio de compra [{p[6]}]: ", p[6])
    nuevo_precio_venta = pedir_float(f"Nuevo precio de venta [{p[7]}]: ", p[7])
    nuevo_stock_actual = pedir_int(f"Nuevo stock actual [{p[8]}]: ", p[8])
    nuevo_stock_minimo = pedir_int(f"Nuevo stock mínimo [{p[9]}]: ", p[9])

    cursor.execute('''
        UPDATE productos
        SET nombre = ?, categoria = ?, marca = ?, presentacion = ?, proveedor = ?,
            precio_compra = ?, precio_venta = ?, stock_actual = ?, stock_minimo = ?
        WHERE id = ?
    ''', (nuevo_nombre, nueva_categoria, nueva_marca, nueva_presentacion, nuevo_proveedor,
          nuevo_precio_compra, nuevo_precio_venta, nuevo_stock_actual, nuevo_stock_minimo, producto_id))

    conn.commit()
    print("✅ Producto actualizado.")
    conn.close()

def eliminar_producto():
    conn = conectar()
    cursor = conn.cursor()
    try:
        producto_id = int(input("ID del producto a eliminar: "))
    except ValueError:
        print("❌ ID inválido.")
        conn.close()
        return

    cursor.execute("SELECT nombre FROM productos WHERE id = ?", (producto_id,))
    p = cursor.fetchone()
    if not p:
        print("❌ Producto no encontrado.")
        conn.close()
        return

    confirmar = input(f"¿Estás seguro de eliminar '{p[0]}'? (s/n): ").lower()
    if confirmar == 's':
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conn.commit()
        print("✅ Producto eliminado.")
    else:
        print("Operación cancelada.")
    conn.close()

def mostrar_stock_bajo():
    conn = conectar()
    cursor = conn.cursor()
    try:
        minimo = int(input("Mostrar productos con stock menor a: "))
    except ValueError:
        print("❌ Valor inválido.")
        conn.close()
        return

    cursor.execute("SELECT id, nombre, stock_actual, stock_minimo FROM productos WHERE stock_actual < ?", (minimo,))
    productos = cursor.fetchall()

    print("\n== Productos con bajo stock ==")
    if productos:
        for p in productos:
            print(f"ID: {p[0]} | {p[1]} | Stock actual: {p[2]} | Stock mínimo: {p[3]}")
    else:
        print("✅ Todos los productos tienen suficiente stock.")
    conn.close()


import sqlite3


def crear_tabla_productos():
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                categoria TEXT,
                marca TEXT,
                presentacion TEXT,
                proveedor TEXT,
                precio_compra REAL NOT NULL,
                precio_venta REAL NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                stock_minimo INTEGER NOT NULL DEFAULT 0
            )
        """)
        conn.commit()
        print("✅ Tabla 'productos' verificada o creada correctamente.")
    except sqlite3.Error as e:
        print(f"❌ Error al crear la tabla productos: {e}")
    finally:
        if conn:
            conn.close()