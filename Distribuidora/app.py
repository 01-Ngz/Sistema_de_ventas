# Archivo principal de línea de comandos
#Funcionalidad:archivo principal para ejecutar desde la terminal.
#Desde aquí, el usuario puede ejecutar comandos como:
"""python app.py agregar_producto
python app.py listar_productos
python app.py registrar_venta
python app.py ver_facturas
python app.py agregar_gasto
python app.py generar_reporte
python app.py ver_stock
python app.py sugerencias_reabastecimiento"""
from finanzas import (
    crear_tabla_finanzas,
    registrar_ingreso,
    registrar_gasto,
    ver_resumen_financiero,
    ver_historial,
    reporte_gastos_por_fecha,
)

from clientes import (
    agregar_cliente,
    listar_clientes,
    buscar_cliente_por_id,
    buscar_cliente_por_nombre,
    editar_cliente,
    eliminar_cliente,
)

from productos import (
    agregar_producto,
    listar_productos,
    buscar_producto_por_id,
    buscar_por_nombre,
    editar_producto,
    eliminar_producto,
    mostrar_stock_bajo,
    crear_tabla_productos
)

from ventas import (  # Asumo que guardaste el código ventas en ventas.py
    registrar_venta,
    eliminar_venta,
    editar_venta,
    top_productos,
    ventas_por_fecha,
    ventas_por_cliente,
)

def safe_float_input(prompt):
    while True:
        valor = input(prompt)
        try:
            return float(valor)
        except ValueError:
            print("❌ Entrada inválida. Por favor, ingresa un número válido.")

def safe_int_input(prompt):
    while True:
        valor = input(prompt)
        try:
            return int(valor)
        except ValueError:
            print("❌ Entrada inválida. Por favor, ingresa un número entero válido.")

def mostrar_menu_finanzas():
    while True:
        print("\n=== MENÚ FINANZAS ===")
        print("1. Registrar ingreso")
        print("2. Registrar gasto")
        print("3. Ver resumen financiero")
        print("4. Ver historial de ingresos")
        print("5. Ver historial de gastos")
        print("6. Reporte de gastos por fecha")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción (0-6): ")

        if opcion == "1":
            monto = safe_float_input("Monto ingreso: ")
            descripcion = input("Descripción ingreso: ")
            origen = input("Origen (default manual): ") or "manual"
            registrar_ingreso(monto, descripcion, origen)

        elif opcion == "2":
            monto = safe_float_input("Monto gasto: ")
            descripcion = input("Descripción gasto: ")
            categoria = input("Categoría (default general): ") or "general"
            registrar_gasto(monto, descripcion, categoria)

        elif opcion == "3":
            ver_resumen_financiero()

        elif opcion == "4":
            ver_historial("ingresos")

        elif opcion == "5":
            ver_historial("gastos")

        elif opcion == "6":
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
            fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
            reporte_gastos_por_fecha(fecha_inicio, fecha_fin)

        elif opcion == "0":
            break
        else:
            print("Opción inválida, intenta nuevamente.")

def menu_clientes():
    while True:
        print("\n--- MENÚ CLIENTES ---")
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por ID")
        print("4. Buscar cliente por nombre")
        print("5. Editar cliente")
        print("6. Eliminar cliente")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción (0-6): ")

        if opcion == '1':
            agregar_cliente()
        elif opcion == '2':
            listar_clientes()
        elif opcion == '3':
            buscar_cliente_por_id()
        elif opcion == '4':
            buscar_cliente_por_nombre()
        elif opcion == '5':
            editar_cliente()
        elif opcion == '6':
            eliminar_cliente()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

def menu_productos():
    while True:
        print("\n--- MENÚ PRODUCTOS ---")
        print("1. Agregar producto")
        print("2. Listar productos")
        print("3. Buscar producto por ID")
        print("4. Buscar producto por nombre")
        print("5. Editar producto")
        print("6. Eliminar producto")
        print("7. Mostrar productos con stock bajo")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción (0-7): ")

        if opcion == '1':
            agregar_producto()
        elif opcion == '2':
            listar_productos()
        elif opcion == '3':
            buscar_producto_por_id()
        elif opcion == '4':
            buscar_por_nombre()
        elif opcion == '5':
            editar_producto()
        elif opcion == '6':
            eliminar_producto()
        elif opcion == '7':
            mostrar_stock_bajo()
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

def menu_ventas():
    while True:
        print("\n--- MENÚ VENTAS ---")
        print("1. Registrar venta")
        print("2. Eliminar venta")
        print("3. Editar venta")
        print("4. Mostrar top productos vendidos")
        print("5. Mostrar ventas por fecha")
        print("6. Mostrar ventas por cliente")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción (0-6): ")

        if opcion == '1':
            registrar_venta()
        elif opcion == '2':
            venta_id = safe_int_input("ID de la venta a cancelar: ")
            eliminar_venta(venta_id)
        elif opcion == '3':
            venta_id = safe_int_input("ID de la venta a editar: ")
            editar_venta(venta_id)
        elif opcion == '4':
            limite = safe_int_input("Cantidad de productos a mostrar en top: ")
            top_productos(limite)
        elif opcion == '5':
            fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
            fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
            ventas_por_fecha(fecha_inicio, fecha_fin)
        elif opcion == '6':
            cliente_id = safe_int_input("ID del cliente: ")
            ventas_por_cliente(cliente_id)
        elif opcion == '0':
            break
        else:
            print("❌ Opción inválida. Intenta de nuevo.")

def mostrar_menu_general():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Finanzas")
    print("2. Clientes")
    print("3. Productos")
    print("4. Ventas")
    print("0. Salir")

def main():
    # Crear tablas si no existen
    try:
        crear_tabla_finanzas()
    except Exception as e:
        print(f"⚠️ Advertencia: No se pudieron crear las tablas financieras. {e}")

    try:
        crear_tabla_productos()
    except Exception as e:
        print(f"⚠️ Advertencia: No se pudo crear la tabla productos. {e}")

    while True:
        mostrar_menu_general()
        opcion = input("Selecciona una opción (0-4): ")

        if opcion == "1":
            mostrar_menu_finanzas()
        elif opcion == "2":
            menu_clientes()
        elif opcion == "3":
            menu_productos()
        elif opcion == "4":
            menu_ventas()
        elif opcion == "0":
            print("Saliendo...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    main()
