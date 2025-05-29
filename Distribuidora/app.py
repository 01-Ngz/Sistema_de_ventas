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
    crear_tablas_finanzas,
    registrar_ingreso,
    registrar_gasto,
    ver_resumen_financiero,
    ver_historial,
    reporte_gastos_por_fecha,
)

def mostrar_menu_finanzas():
    print("\n=== MENÚ FINANZAS ===")
    print("1. Registrar ingreso")
    print("2. Registrar gasto")
    print("3. Ver resumen financiero")
    print("4. Ver historial de ingresos")
    print("5. Ver historial de gastos")
    print("6. Reporte de gastos por fecha")
    print("7. Salir")

def main():
    crear_tablas_finanzas()  # Crear tablas si no existen

    while True:
        mostrar_menu_finanzas()
        opcion = input("Selecciona una opción (1-7): ")

        if opcion == "1":
            monto = float(input("Monto ingreso: "))
            descripcion = input("Descripción ingreso: ")
            origen = input("Origen (default manual): ") or "manual"
            registrar_ingreso(monto, descripcion, origen)

        elif opcion == "2":
            monto = float(input("Monto gasto: "))
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

        elif opcion == "7":
            print("Saliendo...")
            break

        else:
            print("Opción inválida, intenta nuevamente.")

if __name__ == "__main__":
    main()