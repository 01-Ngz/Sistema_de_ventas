import sqlite3
from datetime import datetime

# Conectar o crear la base de datos local
conn = sqlite3.connect("ventas_gaseosas.db")# Crea archivo llamado ()
cursor = conn.cursor() #Cursor es un controlador que permite enviar, instrucciones a la base de datos

# Crear tabla de productos si no existe
#"""#CREA TABLA SI NO EXISTE productos
#   campo     TIPO_DE_DATO                         SIGNIFICADO     
#    id INTEGER PRIMARY KEY AUTOINCREMENT,       #IDENTIFICADOR UNICO DEL PRODUCTO SE CREA AUTOMÁTICAMENTE
#    nombre TEXT NOT NULL,                       #TEXTO NOMBRE DEL PRODUCTO
#    codigo TEXT NOT NULL UNIQUE,                #CODIGO UNICO, NO PUEDE REPETIRSE
#    cantidad INTEGER NOT NULL,                  #CANTIDAD ACTUAL EN INVENTARIO
#    precio_compra REAL NOT NULL,                #PRECIO AL QUE LO COMPRE
#    precio_venta REAL NOT NULL                  #PRECIO AL QUE LO VENDO"""
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (             
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    codigo TEXT NOT NULL UNIQUE,
    cantidad INTEGER NOT NULL,
    precio_compra REAL NOT NULL,
    precio_venta REAL NOT NULL
)
''')

# Crear tabla para ventas
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS ventas (              #CREA TABLA SI NO EXISTE productos
#   campo     TIPO_DE_DATO                         SIGNIFICADO
#    id INTEGER PRIMARY KEY AUTOINCREMENT,        #ID UNICO PARA CADA VENTA
#    codigo TEXT NOT NULL,                        #CODIGO DEL PRODUCTO VENDIDO
#    cantidad INTEGER NOT NULL,                   #CUANTAS UNIDADES SE VENDIERON
#    fecha TEXT NOT NULL                          #CUANDO SE HIZO LA VENTA(En texto)
cursor.execute('''
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    fecha TEXT NOT NULL
)
''')

# Crear tabla para gastos
#cursor.execute('''
#CREATE TABLE IF NOT EXISTS gastos (              #CREA TABLA SI NO EXISTE productos
#   campo     TIPO_DE_DATO                         SIGNIFICADO
#    id INTEGER PRIMARY KEY AUTOINCREMENT,       #ID UNICO DEL GASTO
#    descripcion TEXT NOT NULL,                  #DESCRIPCION DEL GASTO
#    monto REAL NOT NULL,                        #CUANTO COSTO
#    fecha TEXT NOT NULL                         #CUANDO SE HIZO EL GASTO


cursor.execute('''
CREATE TABLE IF NOT EXISTS gastos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descripcion TEXT NOT NULL,
    monto REAL NOT NULL,
    fecha TEXT NOT NULL
)
''')

conn.commit() #Guarda todos los cambios hechos en la base de datos.

# -----------------------------------------------
# Función para agregar un nuevo producto
def agregar_producto():
    nombre = input("Nombre del producto: ")
    codigo = input("Código único del producto: ")
    cantidad = int(input("Cantidad inicial: "))
    precio_compra = float(input("Precio de compra por unidad: "))
    precio_venta = float(input("Precio de venta por unidad: "))

    try:
        cursor.execute("INSERT INTO productos (nombre, codigo, cantidad, precio_compra, precio_venta) VALUES (?, ?, ?, ?, ?)",
                       (nombre, codigo, cantidad, precio_compra, precio_venta))
        conn.commit()
        print("✅ Producto agregado correctamente.")
    except sqlite3.IntegrityError:
        print("❌ Error: El código ya existe. Usa uno diferente.")

# -----------------------------------------------
# Función para buscar un producto
def buscar_producto():
    criterio = input("Buscar por nombre o código: ").lower() #.lower() =Convierte todos los caracteres en minusculas
    cursor.execute("SELECT * FROM productos WHERE nombre LIKE ? OR codigo = ?", (f"%{criterio}%", criterio))
    resultados = cursor.fetchall()

    if resultados:
        for producto in resultados:
            print(f"🔍 {producto}")
    else:
        print("❌ No se encontró ningún producto con ese nombre o código.")

# -----------------------------------------------
#Funcion registrar venta
def registrar_venta(codigo, cantidad):
    cursor.execute('SELECT cantidad FROM productos WHERE codigo = ?', (codigo,))
    resultado = cursor.fetchone()

    if resultado:
        cantidad_disponible = resultado[0]
        if cantidad_disponible >= cantidad:
            # Descontar del inventario
            cursor.execute('UPDATE productos SET cantidad = cantidad - ? WHERE codigo = ?', (cantidad, codigo))

            # Registrar la venta
            fecha_actual = datetime.now().isoformat()
            cursor.execute('''
                INSERT INTO ventas (codigo, cantidad, fecha)
                VALUES (?, ?, ?)
            ''', (codigo, cantidad, fecha_actual))

            conn.commit()
            print("✅ Venta registrada correctamente.")
        else:
            print("⚠️ No hay suficiente inventario.")
    else:
        print("❌ Producto no encontrado.")

# -----------------------------------------------
# Mostrar todos los productos en inventario
def mostrar_inventario():
    cursor.execute("SELECT nombre, codigo, cantidad FROM productos")
    productos = cursor.fetchall()

    print("\n📦 Inventario actual:")
    for producto in productos:
        print(f"Nombre: {producto[0]}, Código: {producto[1]}, Cantidad: {producto[2]}")

# -----------------------------------------------
# Menú principal
def menu():
    while True:
        print("\n--- SISTEMA DE VENTAS DE GASEOSAS ---")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Ver inventario")
        print("4. Registrar venta ")
        print("0. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            agregar_producto()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            mostrar_inventario()
        elif opcion == "4":
            registrar_venta(codigo=  str(input()), cantidad= int(input()))
        elif opcion == "0":
            print("👋 Saliendo...")
            break
        else:
            print("❌ Opción inválida, intenta de nuevo.")

menu()
conn.close()