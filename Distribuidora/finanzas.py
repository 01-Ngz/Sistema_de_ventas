# Ingresos y gastos
#Funcionalidades:Registrar ingresos/gastos, ver flujo de caja

# finanzas.py
import sqlite3
#from datetime import datetime

# Conexión con la base de datos
def conectar():
    return sqlite3.connect('db/gaseosas_distribucion.db')

# Crear tablas de finanzas si no existen
def crear_tablas_finanzas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ingresos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            monto REAL,
            descripcion TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            origen TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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



# -------------------------------------------------------------------------------------------------------------------------------------------
"""✅ Requisitos previos para que funcione
Requisito	                                            Descripción
Base de datos inicializada (gaseosas_distribucion.db)	El archivo de base de datos debe existir (lo creamos desde database.py)
Directorio db/	                                        Asegúrate de tener una carpeta db/ para guardar la base de datos
Crear tablas con crear_tablas_finanzas()	            Llama esta función al inicio para asegurarte que las tablas existen

"""

# ----------------------------------------------------------------------------------------------

"""Tabla de funcionalidades 
Función	                        ¿Qué hace?	                                                     Relación con otros módulos
crear_tablas_finanzas()	    Crea las tablas ingresos y gastos si no existen	Independiente,            se llama una vez
registrar_ingreso()	        Registra un ingreso con descripción y origen	                          Puede ser usado por ventas.py
registrar_gasto()	        Registra un gasto con su categoría y descripción	                      Puede integrarse con inventario o compras
ver_resumen_financiero()	Muestra el total de ingresos, gastos y el balance neto actual	          Ideal para la CLI
ver_historial(tabla)	    Muestra todos los registros de ingresos o gastos	                      Permite control administrativo"""

# ----------------------------------------------------------------------------------------------

"""Sugerencias de futuras mejoras para finanzas
Mejora	                                        ¿Por qué implementarla?
Exportar reportes a Excel o CSV	                Para análisis contable externo o compartir con contador
Visualización gráfica del balance	            Facilita entender el flujo de dinero con gráficos circulares o de barras
Registro de pagos pendientes o deudas	        Control de cuentas por pagar/proveedores
Agregar filtros por fechas o categorías	        Útil para auditoría o revisar gastos específicos
Enlace automático con ventas e inventario	    Que cada venta cree un ingreso automáticamente
Control de caja chica	                        Registrar egresos menores del día a día
Cierre de mes	                                Calcular y registrar el balance mensual automáticamente
"""