# Gestión de clientes
#Funcionalidades:Agregar cliente, ver historial de compras


# clientes.py
import sqlite3


# Conexión a la base de datos
def conectar():
    return sqlite3.connect('db/gaseosas_distribucion.db')


# Agregar un nuevo cliente
def agregar_cliente():
    conn = conectar()
    cursor = conn.cursor()

    nombre = input("Nombre del cliente: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    email = input("Correo electrónico: ")

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
def buscar_cliente(cliente_id):
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


# Editar un cliente
def editar_cliente():
    conn = conectar()
    cursor = conn.cursor()

    cliente_id = int(input("ID del cliente a editar: "))
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


# Eliminar un cliente
def eliminar_cliente():
    conn = conectar()
    cursor = conn.cursor()

    cliente_id = int(input("ID del cliente a eliminar: "))
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
    cliente = cursor.fetchone()

    if cliente:
        confirmar = input(f"¿Estás seguro de eliminar a '{cliente[1]}'? (s/n): ").lower()
        if confirmar == 's':
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conn.commit()
            print("✅ Cliente eliminado.")
    else:
        print("❌ Cliente no encontrado.")

    conn.close()



# ----------------------------------------------------------------------------------------------

"""
Tabla de funcionalidades
Función	               | ¿Qué hace?
agregar_cliente()	       |Registra un nuevo cliente con nombre, dirección, teléfono y correo electrónico.
listar_clientes()	       |Muestra todos los clientes registrados.
buscar_cliente(cliente_id) |Busca un cliente por su ID.
editar_cliente()	       |Permite modificar los datos de un cliente.
eliminar_cliente()	       |Elimina un cliente de la base de datos.
"""