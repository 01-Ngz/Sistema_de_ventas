import os
import sqlite3
from datetime import datetime
from finanzas import registrar_ingreso
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def conectar():
    return sqlite3.connect('gaseosas_distribucion.db')

# ------------------- REGISTRAR VENTA -------------------
def registrar_venta():
    try:
        with conectar() as conn:
            cursor = conn.cursor()

            cliente_id = int(input("ID del cliente que realiza la compra: "))
            cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                print("❌ Cliente no encontrado.")
                return

            carrito = []
            while True:
                try:
                    producto_id = int(input("ID del producto a vender: "))
                    cantidad = int(input("Cantidad: "))
                except ValueError:
                    print("❌ Entrada inválida. Usa solo números.")
                    continue

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

            if not carrito:
                print("❌ No se agregó ningún producto.")
                return

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
                cursor.execute('''
                    UPDATE productos
                    SET stock_actual = stock_actual - ?
                    WHERE id = ?
                ''', (cantidad, producto_id))

            registrar_ingreso(total, f"Venta ID #{venta_id}", origen="venta")
            print(f"✅ Venta registrada con ID {venta_id} y total ${total:.2f}")

    except Exception as e:
        print(f"❌ Error al registrar venta: {e}")

# ------------------- CANCELAR VENTA -------------------
def eliminar_venta(venta_id):
    try:
        with conectar() as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM ventas WHERE id = ?", (venta_id,))
            venta = cursor.fetchone()
            if not venta:
                print("❌ Venta no encontrada.")
                return

            cursor.execute("SELECT producto_id, cantidad FROM detalle_ventas WHERE venta_id = ?", (venta_id,))
            productos = cursor.fetchall()

            for producto_id, cantidad in productos:
                cursor.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id = ?", (cantidad, producto_id))

            cursor.execute("DELETE FROM detalle_ventas WHERE venta_id = ?", (venta_id,))
            cursor.execute("DELETE FROM ventas WHERE id = ?", (venta_id,))

            print(f"✅ Venta {venta_id} cancelada y stock restaurado.")
    except Exception as e:
        print(f"❌ Error al cancelar venta: {e}")

# ------------------- EDITAR VENTA -------------------
def editar_venta(venta_id):
    try:
        cancelar_venta(venta_id)  # Borra la venta actual
        print("Ingrese los nuevos datos para la venta:")
        registrar_venta()         # Registra una nueva venta
    except Exception as e:
        print(f"❌ Error al editar venta: {e}")

# ------------------- TOP PRODUCTOS VENDIDOS -------------------
def top_productos(limit=5):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.nombre, SUM(d.cantidad) as total_vendidos
                FROM detalle_ventas d
                JOIN productos p ON d.producto_id = p.id
                GROUP BY d.producto_id
                ORDER BY total_vendidos DESC
                LIMIT ?
            ''', (limit,))
            resultados = cursor.fetchall()

            print("\n== TOP PRODUCTOS VENDIDOS ==")
            for i, (nombre, total) in enumerate(resultados, 1):
                print(f"{i}. {nombre} - {total} unidades")
    except Exception as e:
        print(f"❌ Error al obtener top productos: {e}")

# ------------------- VENTAS POR FECHA -------------------
def ventas_por_fecha(fecha_inicio, fecha_fin):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT v.id, c.nombre, v.fecha, v.total
                FROM ventas v
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.fecha BETWEEN ? AND ?
                ORDER BY v.fecha ASC
            ''', (fecha_inicio, fecha_fin))
            ventas = cursor.fetchall()

            print("\n== VENTAS POR FECHA ==")
            for v in ventas:
                print(f"ID: {v[0]} | Cliente: {v[1]} | Fecha: {v[2]} | Total: ${v[3]:.2f}")
    except Exception as e:
        print(f"❌ Error al consultar ventas por fecha: {e}")

# ------------------- VENTAS POR CLIENTE -------------------
def ventas_por_cliente(cliente_id):
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, fecha, total FROM ventas
                WHERE cliente_id = ?
                ORDER BY fecha DESC
            ''', (cliente_id,))
            ventas = cursor.fetchall()

            print(f"\n== VENTAS DEL CLIENTE {cliente_id} ==")
            for v in ventas:
                print(f"ID: {v[0]} | Fecha: {v[1]} | Total: ${v[2]:.2f}")
    except Exception as e:
        print(f"❌ Error al consultar ventas del cliente: {e}")

# ------------------- EXPORTAR FACTURA A PDF -------------------

"""exportar_factura_pdf(venta_id)
Donde venta_id es el ID de la venta que quieres exportar a PDF."""
def exportar_factura_pdf(venta_id):
    os.makedirs('facturas', exist_ok=True)
    nombre_pdf = f"facturas/factura_venta_{venta_id}.pdf"

    try:
        with conectar() as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT v.id, v.fecha, v.total, c.nombre, c.direccion, c.telefono
                FROM ventas v
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.id = ?
            ''', (venta_id,))
            venta = cursor.fetchone()
            if not venta:
                print("❌ Venta no encontrada.")
                return

            cursor.execute('''
                SELECT p.nombre, d.cantidad, d.precio_unitario, d.subtotal
                FROM detalle_ventas d
                JOIN productos p ON d.producto_id = p.id
                WHERE d.venta_id = ?
            ''', (venta_id,))
            productos = cursor.fetchall()

        c = canvas.Canvas(nombre_pdf, pagesize=letter)
        width, height = letter

        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, height - 50, "Factura de Venta")
        c.setFont("Helvetica", 12)
        c.drawString(50, height - 80, f"ID Venta: {venta[0]}")
        c.drawString(50, height - 100, f"Fecha: {venta[1]}")
        c.drawString(50, height - 120, f"Cliente: {venta[3]}")
        c.drawString(50, height - 140, f"Dirección: {venta[4] if venta[4] else 'N/A'}")
        c.drawString(50, height - 160, f"Teléfono: {venta[5] if venta[5] else 'N/A'}")

        c.drawString(50, height - 190, "Productos:")
        y = height - 210
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Nombre")
        c.drawString(250, y, "Cantidad")
        c.drawString(320, y, "Precio Unitario")
        c.drawString(430, y, "Subtotal")
        y -= 15
        c.setFont("Helvetica", 10)

        for nombre, cantidad, precio_unitario, subtotal in productos:
            c.drawString(50, y, str(nombre))
            c.drawString(250, y, str(cantidad))
            c.drawString(320, y, f"${precio_unitario:.2f}")
            c.drawString(430, y, f"${subtotal:.2f}")
            y -= 15
            if y < 50:
                c.showPage()
                y = height - 50

        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y - 10, f"Total a pagar: ${venta[2]:.2f}")

        c.save()
        print(f"✅ Factura PDF generada: {nombre_pdf}")
    except Exception as e:
        print(f"❌ Error al generar factura PDF: {e}")

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

"""📌 Requisitos para que funcione
Tener los productos cargados en productos.

Tener clientes cargados (o usar cliente_id = 0 para venta directa).

Tener creada la base de datos (database.py).

Tener tabla inventario_movimientos creada (ya lo hicimos antes).
"""

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