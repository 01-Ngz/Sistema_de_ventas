# Ingresos y gastos
#Funcionalidades:Registrar ingresos/gastos, ver flujo de caja

# finanzas.py
import sqlite3
import os

# Conexión con la base de datos
def conectar():
    # Asegura que la carpeta 'db/' exista
    os.makedirs("db", exist_ok=True)

    db_path = "gaseosas_distribucion.db"

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
def crear_tabla_finanzas():
    conn = sqlite3.connect("distribuidora.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS finanzas (
            registro_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT CHECK(tipo IN ('ingreso', 'gasto')) NOT NULL,
            monto REAL NOT NULL,
            descripcion TEXT,
            origen TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()


# Registrar un ingreso manual o automático (por venta, por ejemplo)
def registrar_ingreso(monto, descripcion, origen="manual"):
    conn = None
    try:
        monto = float(monto)
        if monto <= 0:
            raise ValueError("El monto debe ser positivo.")

        conn = sqlite3.connect("distribuidora.db")
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO finanzas (tipo, monto, descripcion, origen)
            VALUES ('ingreso', ?, ?, ?)
        ''', (monto, descripcion, origen))

        conn.commit()
        print("Ingreso registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar ingreso: {e}")
    finally:
        if conn:
            conn.close()


# Registrar un gasto
def registrar_gasto(monto, descripcion, categoria="general"):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO finanzas (monto, descripcion, categoria, tipo)
        VALUES (?, ?, ?, 'gasto')
    ''', (monto, descripcion, categoria))

    conn.commit()
    conn.close()
    print("✅ Gasto registrado correctamente.")


# Ver resumen financiero


    conn.close()


# Ver historial de ingresos o gastos
def ver_historial(tipo="ingreso"):
    conn = sqlite3.connect("distribuidora.db")
    cursor = conn.cursor()

    cursor.execute('''
        SELECT registro_id, monto, descripcion, fecha, origen 
        FROM finanzas 
        WHERE tipo = ? 
        ORDER BY fecha DESC
    ''', (tipo,))

    filas = cursor.fetchall()

    if not filas:
        print(f"No hay registros de {tipo}s.")
    else:
        print(f"\n--- HISTORIAL DE {tipo.upper()}S ---")
        for fila in filas:
            print(f"ID: {fila[0]}, Monto: ${fila[1]:.2f}, Desc: {fila[2]}, Fecha: {fila[3]}, Origen: {fila[4]}")

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
def ver_resumen_financiero():
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
        print(f"ID: {gasto[0]} | Monto: ${gasto[1]:.2f} | Descripción: {gasto[2]} | Fecha: {gasto[3]} | Origen: {gasto[4]}")



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

"""

#Daño en resumen financiero: sale otra base de datos