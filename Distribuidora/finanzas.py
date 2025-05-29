# Ingresos y gastos
#Funcionalidades:Registrar ingresos/gastos, ver flujo de caja

# finanzas.py
import sqlite3
import os

# Conexión con la base de datos
def conectar():
    # Asegura que la carpeta 'db/' exista
    os.makedirs("db", exist_ok=True)

    db_path = "db/gaseosas_distribucion.db"

    # Si el archivo existe y está dañado, lo borramos
    if os.path.exists(db_path):
        try:
            # Intentamos abrir y consultar algo mínimo
            conn = sqlite3.connect(db_path)
            conn.execute("SELECT name FROM sqlite_master LIMIT 1")
            conn.close()
        except sqlite3.DatabaseError:
            print("⚠️ Archivo de base de datos dañado. Se eliminará y recreará.")
            os.remove(db_path)

    # Conectamos (creará la DB si no existe)
    return sqlite3.connect(db_path)

# Crear tablas de finanzas si no existen
def crear_tablas_finanzas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL,
            descripcion TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            origen TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL,
            descripcion TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            categoria TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Registrar un ingreso manual o automático (por venta, por ejemplo)
def registrar_ingreso(monto, descripcion, origen="manual"):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO ingresos (monto, descripcion, origen)
        VALUES (?, ?, ?)
    ''', (monto, descripcion, origen))

    conn.commit()
    conn.close()
    print("✅ Ingreso registrado correctamente.")


# Registrar un gasto
def registrar_gasto(monto, descripcion, categoria="general"):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO gastos (monto, descripcion, categoria)
        VALUES (?, ?, ?)
    ''', (monto, descripcion, categoria))

    conn.commit()
    conn.close()
    print("✅ Gasto registrado correctamente.")


# Ver resumen financiero
def ver_resumen_financiero():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(monto) FROM ingresos')
    total_ingresos = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(monto) FROM gastos')
    total_gastos = cursor.fetchone()[0] or 0

    balance = total_ingresos - total_gastos

    print("📊 Resumen Financiero")
    print(f"Ingresos Totales: ${total_ingresos:.2f}")
    print(f"Gastos Totales:   ${total_gastos:.2f}")
    print(f"Balance Neto:     ${balance:.2f}")

    conn.close()


# Ver historial de ingresos o gastos
def ver_historial(tabla):
    conn = conectar()
    cursor = conn.cursor()

    if tabla == 'ingresos':
        cursor.execute('SELECT * FROM ingresos ORDER BY fecha DESC')
    elif tabla == 'gastos':
        cursor.execute('SELECT * FROM gastos ORDER BY fecha DESC')
    else:
        print("❌ Tabla no válida. Usa 'ingresos' o 'gastos'.")
        return

    registros = cursor.fetchall()

    print(f"📄 Historial de {tabla}:")
    for r in registros:
        print(f"#{r[0]} | ${r[1]} | {r[2]} | {r[3]} | {r[4] if len(r) > 4 else ''}")

    conn.close()


# Ver todos los gastos registrados
def ver_gastos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT registro_id, monto, descripcion, fecha, origen
        FROM finanzas
        WHERE tipo = 'gasto'
        ORDER BY fecha DESC
    ''')

    gastos = cursor.fetchall()
    conn.close()

    print("== Historial de gastos ==")
    for gasto in gastos:
        print(f"ID: {gasto[0]} | Monto: ${gasto[1]:.2f} | Descripción: {gasto[2]} | Fecha: {gasto[3]} | Origen: {gasto[4]}")

# Reporte resumen financiero: total ingresos, total gastos, y ganancia neta
def reporte_resumen_financiero():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('SELECT SUM(monto) FROM finanzas WHERE tipo = "ingreso"')
    total_ingresos = cursor.fetchone()[0] or 0

    cursor.execute('SELECT SUM(monto) FROM finanzas WHERE tipo = "gasto"')
    total_gastos = cursor.fetchone()[0] or 0

    ganancia_neta = total_ingresos - total_gastos

    print("\n=== Resumen Financiero ===")
    print(f"Total Ingresos: ${total_ingresos:.2f}")
    print(f"Total Gastos:   ${total_gastos:.2f}")
    print(f"Ganancia Neta:  ${ganancia_neta:.2f}\n")

    conn.close()

# Reporte de gastos filtrado por fecha (rango)
def reporte_gastos_por_fecha(fecha_inicio, fecha_fin):
    """
    Muestra gastos registrados entre fecha_inicio y fecha_fin.
    Formato fechas: 'YYYY-MM-DD'
    """
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT registro_id, monto, descripcion, fecha, origen
        FROM finanzas
        WHERE tipo = 'gasto' AND date(fecha) BETWEEN ? AND ?
        ORDER BY fecha DESC
    ''', (fecha_inicio, fecha_fin))

    gastos = cursor.fetchall()
    conn.close()

    print(f"\n== Gastos desde {fecha_inicio} hasta {fecha_fin} ==")
    for gasto in gastos:
        print(f"ID: {gasto[0]} | Monto: ${gasto[1]:.2f} | Descripción: {gasto[2]} | Fecha: {gasto[3]} | Origen: {gasto[4]}"

"""
-- Gestión de ingresos, gastos y reportes financieros

Funciones principales para:
- Registrar ingresos y gastos
- Consultar historial
- Generar reportes financieros básicos

---

Requisitos previos para que funcione:
- La base de datos SQLite debe estar creada y accesible en 'db/gaseosas_distribucion.db'
- La carpeta 'db/' debe existir y tener permisos de escritura
- Python instalado con el módulo sqlite3 (incluido en la mayoría de distribuciones)
- El archivo debe ejecutarse en un entorno donde se permita la lectura y escritura de archivos

---

Sugerencias de futuras mejoras:
- Validar entradas para evitar datos negativos o mal formateados
- Unificar las tablas ingresos y gastos en una sola tabla con campo "tipo" para simplificar consultas
- Añadir autenticación de usuarios para controlar quién registra ingresos/gastos
- Incorporar edición y eliminación de registros para corrección de errores
- Mejorar reportes con filtros por categorías, usuarios o rangos más específicos
- Exportar reportes a formatos como CSV o PDF para análisis externo
- Añadir gráficos y visualizaciones usando librerías como matplotlib o seaborn
- Automatizar registros vinculados a ventas y compras para evitar registros manuales
- Crear un CLI o interfaz web para manejar finanzas de forma amigable

---

| Función                    | ¿Qué hace?                                                                |
|---------------------------|--------------------------------------------------------------------------- |
| creasto()                          | Inserta un nuevo gasto en la base de datos                                |
| ver_resumen_tablas_finanzas()    | Crea las tablas 'ingresos' y 'gastos' si no existen                       |
| registrar_ingreso()                | Inserta un nuevo ingreso en la base de datos                              |
| registrar_g_financiero()           | Muestra totales de ingresos, gastos y balance neto                        |
| ver_historial(tabla)               | Lista todos los registros de la tabla especificada ('ingresos' o 'gastos')|
| ver_gastos()                       |(Función parcialmente repetida) Muestra todos los gastos                   |
| reporte_resumen_financiero()       | (Función parcialmente repetida) Muestra resumen consolidado               |
| reporte_gastos_por_fecha()         | Muestra gastos dentro de un rango de fechas                               |

""")