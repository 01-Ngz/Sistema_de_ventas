# Funciones para productos, gestiona productos.
#Funcionalidades:Agregar, editar, eliminar, listar, buscar producto

# productos.py
import sqlite3


# Conexión a la base de datos
def conectar():
    return sqlite3.connect('db/gaseosas_distribucion.db')


# Agregar un nuevo producto
def agregar_producto():
    conn = conectar()
    cursor = conn.cursor()

    nombre = input("Nombre del producto: ")
    descripcion = input("Descripción: ")
    precio_compra = float(input("Precio de compra: "))
    precio_venta = float(input("Precio de venta: "))
    stock_actual = int(input("Stock actual: "))

    cursor.execute('''
        INSERT INTO productos (nombre, descripcion, precio_compra, precio_venta, stock_actual)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, descripcion, precio_compra, precio_venta, stock_actual))

    conn.commit()
    conn.close()
    print("✅ Producto agregado correctamente.")


# Listar todos los productos
def listar_productos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, stock_actual, precio_venta FROM productos")
    productos = cursor.fetchall()

    print("\n== Lista de productos ==")
    for p in productos:
        print(f"ID: {p[0]} | Nombre: {p[1]} | Stock: {p[2]} | Precio venta: ${p[3]}")

    conn.close()


# Buscar un producto por ID
def buscar_producto(producto_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if producto:
        print("\n== Detalles del producto ==")
        print(f"ID: {producto[0]}")
        print(f"Nombre: {producto[1]}")
        print(f"Descripción: {producto[2]}")
        print(f"Precio compra: {producto[3]}")
        print(f"Precio venta: {producto[4]}")
        print(f"Stock actual: {producto[5]}")
    else:
        print("❌ Producto no encontrado.")

    conn.close()


# Buscar productos por nombre (parcial)
def buscar_por_nombre():
    conn = conectar()
    cursor = conn.cursor()

    nombre = input("Buscar por nombre (parcial): ")
    cursor.execute("SELECT id, nombre, stock_actual FROM productos WHERE nombre LIKE ?", (f"%{nombre}%",))
    productos = cursor.fetchall()

    if productos:
        print("\n== Resultados de búsqueda ==")
        for p in productos:
            print(f"ID: {p[0]} | Nombre: {p[1]} | Stock: {p[2]}")
    else:
        print("❌ No se encontraron productos con ese nombre.")

    conn.close()


# Editar un producto existente
def editar_producto():
    conn = conectar()
    cursor = conn.cursor()

    producto_id = int(input("ID del producto a editar: "))
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if producto:
        print("Deja en blanco si no deseas cambiar un campo.\n")
        nuevo_nombre = input(f"Nuevo nombre [{producto[1]}]: ") or producto[1]
        nueva_descripcion = input(f"Nueva descripción [{producto[2]}]: ") or producto[2]
        nuevo_precio_compra = input(f"Nuevo precio de compra [{producto[3]}]: ") or producto[3]
        nuevo_precio_venta = input(f"Nuevo precio de venta [{producto[4]}]: ") or producto[4]
        nuevo_stock = input(f"Nuevo stock [{producto[5]}]: ") or producto[5]

        cursor.execute('''
            UPDATE productos
            SET nombre = ?, descripcion = ?, precio_compra = ?, precio_venta = ?, stock_actual = ?
            WHERE id = ?
        ''', (nuevo_nombre, nueva_descripcion, float(nuevo_precio_compra),
              float(nuevo_precio_venta), int(nuevo_stock), producto_id))

        conn.commit()
        print("✅ Producto actualizado.")
    else:
        print("❌ Producto no encontrado.")

    conn.close()


# Eliminar un producto
def eliminar_producto():
    conn = conectar()
    cursor = conn.cursor()

    producto_id = int(input("ID del producto a eliminar: "))
    cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if producto:
        confirmar = input(f"¿Estás seguro de eliminar '{producto[1]}'? (s/n): ").lower()
        if confirmar == 's':
            cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
            conn.commit()
            print("✅ Producto eliminado.")
    else:
        print("❌ Producto no encontrado.")

    conn.close()


# Mostrar productos con bajo stock
def mostrar_stock_bajo():
    conn = conectar()
    cursor = conn.cursor()

    minimo = int(input("Mostrar productos con stock menor a: "))
    cursor.execute("SELECT id, nombre, stock_actual FROM productos WHERE stock_actual < ?", (minimo,))
    productos = cursor.fetchall()

    print("\n== Productos con bajo stock ==")
    if productos:
        for p in productos:
            print(f"ID: {p[0]} | {p[1]} | Stock actual: {p[2]}")
    else:
        print("✅ Todos los productos tienen suficiente stock.")

    conn.close()



# ----------------------------------------------------------------------------------------------
"""Función	¿Qué hace?
agregar_producto()	            |Agrega un nuevo producto a la base de datos con nombre, descripción, precio de compra, venta y stock inicial.
listar_productos()	            |Muestra todos los productos disponibles con su información básica (ID, nombre, precio, stock).
buscar_producto(producto_id)	|Busca un producto específico por su ID y muestra su información.
(en futuras versiones)	      Se puede agregar: editar, eliminar, filtrar por stock bajo, buscar por nombre.
editar_producto()	            |Permite cambiar nombre, precio, descripción o stock de un producto.
eliminar_producto()	            |Elimina un producto de la base de datos.
buscar_por_nombre()	            |Busca productos escribiendo parte del nombre.
mostrar_stock_bajo()	        |Muestra productos con poco stock (stock < mínimo definido).
"""


#realizar menu