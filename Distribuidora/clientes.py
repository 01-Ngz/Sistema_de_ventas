# Gestión de clientes
#Funcionalidades:Agregar cliente, ver historial de compras
# clientes.py
import sqlite3

# Conexión a la base de datos
def conectar():
    return sqlite3.connect('gaseosas_distribucion.db')

# Agregar un nuevo cliente
def agregar_cliente():
    conn = conectar()
    cursor = conn.cursor()

    nombre = input("Nombre del cliente: ").strip()
    direccion = input("Dirección: ").strip()
    telefono = input("Teléfono: ").strip()
    email = input("Correo electrónico: ").strip()

    if not nombre:
        print("❌ El nombre es obligatorio.")
        return

    cursor.execute('''
        INSERT INTO clientes (nombre, direccion, telefono, email)
        VALUES (?, ?, ?, ?)
    ''', (nombre, direccion, telefono, email))

    conn.commit()
    conn.close()
    print("✅ Cliente agregado exitosamente.")

# Listar todos los clientes
def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nombre, telefono FROM clientes")
    clientes = cursor.fetchall()

    print("\n== Lista de clientes ==")
    for c in clientes:
        print(f"ID: {c[0]} | Nombre: {c[1]} | Teléfono: {c[2]}")

    conn.close()

# Buscar cliente por ID
def buscar_cliente_por_id():
    try:
        cliente_id = int(input("ID del cliente: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    if cliente:
        print("\n== Detalles del cliente ==")
        print(f"ID: {cliente[0]}")
        print(f"Nombre: {cliente[1]}")
        print(f"Dirección: {cliente[2]}")
        print(f"Teléfono: {cliente[3]}")
        print(f"Email: {cliente[4]}")
    else:
        print("❌ Cliente no encontrado.")

    conn.close()

# Buscar cliente por nombre (NUEVA FUNCIÓN)
def buscar_cliente_por_nombre():
    nombre = input("Nombre del cliente a buscar: ").strip()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ?", (f'%{nombre}%',))
    clientes = cursor.fetchall()

    if clientes:
        print("\n== Resultados de la búsqueda ==")
        for c in clientes:
            print(f"ID: {c[0]} | Nombre: {c[1]} | Teléfono: {c[3]} | Email: {c[4]}")
    else:
        print("❌ No se encontraron coincidencias.")

    conn.close()

# Editar cliente
def editar_cliente():
    try:
        cliente_id = int(input("ID del cliente a editar: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    if cliente:
        print("Deja en blanco si no deseas cambiar un campo.\n")
        nuevo_nombre = input(f"Nuevo nombre [{cliente[1]}]: ") or cliente[1]
        nueva_direccion = input(f"Nueva dirección [{cliente[2]}]: ") or cliente[2]
        nuevo_telefono = input(f"Nuevo teléfono [{cliente[3]}]: ") or cliente[3]
        nuevo_email = input(f"Nuevo email [{cliente[4]}]: ") or cliente[4]

        cursor.execute('''
            UPDATE clientes
            SET nombre = ?, direccion = ?, telefono = ?, email = ?
            WHERE id = ?
        ''', (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_email, cliente_id))

        conn.commit()
        print("✅ Cliente actualizado.")
    else:
        print("❌ Cliente no encontrado.")

    conn.close()

# Eliminar cliente
def eliminar_cliente():
    try:
        cliente_id = int(input("ID del cliente a eliminar: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    if cliente:
        confirmar = input(f"¿Estás seguro de eliminar a '{cliente[1]}'? (s/n): ").lower()
        if confirmar == 's':
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conn.commit()
            print("✅ Cliente eliminado.")
        else:
            print("❌ Eliminación cancelada.")
    else:
        print("❌ Cliente no encontrado.")

    conn.close()



# Menú CLI
def menu_clientes():
    while True:
        print("\n--- Menú de Clientes ---")
        print("1. Agregar cliente")
        print("2. Listar clientes")
        print("3. Buscar cliente por ID")
        print("4. Buscar cliente por nombre")
        print("5. Editar cliente")
        print("6. Eliminar cliente")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

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

# Puedes llamar menu_clientes() desde el archivo principal si lo deseas.
#Busco llamar la function Menu_Clientes y se hay escoger cualquiera de estas subfunciones
# ----------------------------------------------------------------------------------------------

"""
Tabla de funcionalidades
Función	                   | ¿Qué hace?
agregar_cliente()	       |Registra un nuevo cliente con nombre, dirección, teléfono y correo electrónico.
listar_clientes()	       |Muestra todos los clientes registrados.
buscar_cliente(cliente_id) |Busca un cliente por su ID.
buscar_cliente(nombre)     |Busca un cliente por su nombre
editar_cliente()	       |Permite modificar los datos de un cliente.
eliminar_cliente()	       |Elimina un cliente de la base de datos.

"""

#realizar menu