# Conexión y creación de tablas
#funcionalidades: crea y conecta la base de datos.

# database.py
import sqlite3

# Esta función conecta con la base de datos y crea todas las tablas necesarias
def crear_base_datos():
    conn = sqlite3.connect('db/gaseosas_distribucion.db')  # Crea la base de datos si no existe
    cursor = conn.cursor()

    # Crear tabla de usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('admin', 'vendedor', 'contador')),
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Crear tabla de clientes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        tipo TEXT DEFAULT 'minorista',
        zona TEXT,
        contacto TEXT
    )
    ''')

    # Crear tabla de productos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        marca TEXT,
        presentacion TEXT,
        proveedor TEXT,
        precio_compra REAL NOT NULL,
        precio_venta REAL NOT NULL,
        stock_actual INTEGER NOT NULL DEFAULT 0,
        stock_minimo INTEGER DEFAULT 0,
        activo INTEGER DEFAULT 1,
        creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Crear tabla de lotes para control por fecha de vencimiento
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS lotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        cantidad INTEGER,
        fecha_ingreso DATE,
        fecha_vencimiento DATE,
        FOREIGN KEY (producto_id) REFERENCES productos(id)
    )
    ''')

    # Movimientos de inventario
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventario_movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto_id INTEGER,
        tipo TEXT CHECK(tipo IN ('entrada', 'salida', 'ajuste')),
        cantidad INTEGER,
        motivo TEXT,
        usuario_id INTEGER,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (producto_id) REFERENCES productos(id),
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("Base de datos creada correctamente.")