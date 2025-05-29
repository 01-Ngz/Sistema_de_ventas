# Registro de ventas y facturación
#Funcionalidades: Registrar venta, generar factura interna, ver ventas

# ventas.py
import sqlite3
from datetime import datetime
from finanzas import registrar_ingreso

def conectar():
    return sqlite3.connect('db/gaseosas_distribucion.db')

# Registrar una nueva venta
def registrar_venta():
    conn = conectar()
    cursor = conn.cursor()

    cliente_id = int(input("ID del cliente que realiza la compra: "))
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()
    if not cliente:
        print("❌ Cliente no encontrado.")
        conn.close()
        return

    carrito = []
    while True:
        producto_id = int(input("ID del producto a vender: "))
        cantidad = int(input("Cantidad: "))

        cursor.execute("SELECT nombre, precio_venta, stock_actual FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()
        if not producto:
            print("❌ Producto no encontrado.")
            continue
        if cantidad > producto[2]:
            print("❌ No hay suficiente stock.")
            continue

        subtotal = cantidad * producto[1]
        carrito.append((producto_id, cantidad, producto[1], subtotal))

        seguir = input("¿Agregar otro producto? (s/n): ").lower()
        if seguir != 's':
            break

    total = sum(item[3] for item in carrito)
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT INTO ventas (cliente_id, fecha, total)
        VALUES (?, ?, ?)
    ''', (cliente_id, fecha, total))
    venta_id = cursor.lastrowid

    for producto_id, cantidad, precio_unitario, subtotal in carrito:
        cursor.execute('''
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        ''', (venta_id, producto_id, cantidad, precio_unitario, subtotal))

        # Actualizar stock
        cursor.execute('''
            UPDATE productos
            SET stock_actual = stock_actual - ?
            WHERE id = ?
        ''', (cantidad, producto_id))

    conn.commit()
    conn.close()
    print(f"✅ Venta registrada con ID {venta_id} y total ${total:.2f}")


def calcular_total(productos_vendidos):
    total = 0
    for producto in productos_vendidos:
        cantidad = producto["cantidad"]
        precio_unitario = producto["precio_unitario"]
        total += cantidad * precio_unitario
    return total

# Guarda la venta principal y los productos vendidos en la base de datos
def guardar_venta_en_bd(cliente_id, productos_vendidos):
    conn = conectar()
    cursor = conn.cursor()

    total = calcular_total(productos_vendidos)

    # Guardar venta principal
    cursor.execute('''
        INSERT INTO ventas (cliente_id, total)
        VALUES (?, ?)
    ''', (cliente_id, total))

    venta_id = cursor.lastrowid  # obtener el ID de la venta recién creada

    # Guardar detalles de productos
    for producto in productos_vendidos:
        producto_id = producto["producto_id"]
        cantidad = producto["cantidad"]
        precio_unitario = producto["precio_unitario"]
        subtotal = cantidad * precio_unitario

        cursor.execute('''
            INSERT INTO detalles_venta (venta_id, producto_id, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        ''', (venta_id, producto_id, cantidad, precio_unitario, subtotal))

    conn.commit()
    conn.close()

    # Registrar automáticamente el ingreso en finanzas
    descripcion = f"Venta ID #{venta_id}"
    registrar_ingreso(total, descripcion, origen="venta")

    return venta_id

# Generar factura interna de una venta
def generar_factura(venta_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT ventas.id, clientes.nombre, ventas.fecha, ventas.total
        FROM ventas
        JOIN clientes ON ventas.cliente_id = clientes.id
        WHERE ventas.id = ?
    ''', (venta_id,))
    venta = cursor.fetchone()

    if not venta:
        print("❌ Venta no encontrada.")
        conn.close()
        return

    print("\n📄 FACTURA INTERNA")
    print(f"ID Venta: {venta[0]}")
    print(f"Cliente: {venta[1]}")
    print(f"Fecha: {venta[2]}")
    print("===================================")

    cursor.execute('''
        SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
        FROM detalle_ventas d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.venta_id = ?
    ''', (venta_id,))
    detalles = cursor.fetchall()

    for item in detalles:
        print(f"{item[0]} - Cant: {item[1]} x ${item[2]} = ${item[3]:.2f}")

    print("===================================")
    print(f"TOTAL: ${venta[3]:.2f}")
    conn.close()

# Listar todas las ventas
def listar_ventas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT v.id, c.nombre, v.fecha, v.total
        FROM ventas v
        JOIN clientes c ON v.cliente_id = c.id
        ORDER BY v.fecha DESC
    ''')
    ventas = cursor.fetchall()

    print("\n== HISTORIAL DE VENTAS ==")
    for v in ventas:
        print(f"ID: {v[0]} | Cliente: {v[1]} | Fecha: {v[2]} | Total: ${v[3]:.2f}")

    conn.close()

# Ver detalle de una venta
def detalle_venta(venta_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
        FROM detalle_ventas d
        JOIN productos p ON d.producto_id = p.id
        WHERE d.venta_id = ?
    ''', (venta_id,))
    detalles = cursor.fetchall()

    if detalles:
        print("\n== Detalle de venta ==")
        for d in detalles:
            print(f"{d[0]} - {d[1]} unidades x ${d[2]} = ${d[3]}")
    else:
        print("❌ No hay detalles para esta venta.")

    conn.close()


# ----------------------------------------------------------------------------------------------

"""Función	                                                    ¿Qué hace?.	                                                                                                        ¿Dónde se usa?	                        Relación con otras funcionalidades
conectar()	                                    Conecta con la base de datos SQLite (gaseosas_distribucion.db).	                                                                En todas las funciones	                Parte de la infraestructura base del sistema
crear_tablas_ventas()	                        Crea las tablas ventas y detalles_venta si no existen.	                                                                        Al iniciar el sistema	                Depende del módulo clientes y productos por sus FOREIGN KEY
calcular_total(productos)	                    Calcula el total a pagar por los productos vendidos (cantidad × precio).	                                                    Usada en guardar_venta_en_bd()	        Facilita el cálculo del monto total en cada venta
descontar_inventario(productos)	                Resta la cantidad vendida al stock actual del producto y registra un movimiento de salida en inventario_movimientos.	        Después de cada venta	                Relacionado al módulo de inventario
guardar_venta_en_bd(cliente_id, productos)	    Guarda una venta y los detalles de cada producto vendido (cantidad, precio, subtotal).	                                        Usada por registrar_venta()	            Relacionado a ventas, detalles_venta, productos, clientes
generar_factura(venta_id)	                    Muestra una factura detallada con productos, precios unitarios, subtotales, total y nombre del cliente.	                        Después de guardar una venta	        Mejora el control interno y puede adaptarse a impresión
registrar_venta()	                            Ejecuta el flujo completo de venta: solicita datos, busca precios, registra en DB, descuenta inventario y genera factura.	    Uso directo (por CLI en el futuro)	    Usa casi todas las funciones anteriores
ver_ventas()	                                Muestra todas las ventas anteriores con su ID, nombre del cliente, total y fecha.	                                            Consultas administrativas	            Útil para auditoría, análisis de ventas"""

# -----------------------------------------------

"""📌 Requisitos previos para que funcione
Tener los productos cargados en productos.

Tener clientes cargados (o usar cliente_id = 0 para venta directa).

Tener creada la base de datos (database.py).

Tener tabla inventario_movimientos creada (ya lo hicimos antes)."""

#️ Sugerencias de futuras mejoras, Requisitos previos para que funcione, Tabla de Funcionalidades

"""🛠️ Sugerencias de futuras mejoras
Mejora	Descripción
Cancelar venta	Eliminar venta y reponer stock automáticamente
Editar venta	Modificar cantidades o productos vendidos (controlado con historial)
Exportar factura a PDF o CSV	Para impresión, envío o respaldo externo
Reportes por fechas o cliente	Ventas filtradas por período o por comprador
Top productos vendidos	Saber cuáles gaseosas se venden más
Integrar con ingresos (contabilidad)	Cada venta registra automáticamente ingreso en módulo contable"""


#realizar menu