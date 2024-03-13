import mysql.connector
#pip install mysql-connector-python

# Configuración de la conexión a la base de datos
config = {
    'host': 'localhost',
    'user': 'vale',
    'password': 'Salem31ob',
    'database': 'prueba'
}

# Conectar a la base de datos
conexion = mysql.connector.connect(**config)

# cursor para ejecutar consultas
cursor = conexion.cursor()

try:
    # Solicitar ingresar datos
    a_nombre = input("Ingrese el nuevo nombre: ")
    a_edad = int(input("Ingrese la nueva edad: "))

    # Consulta de inserción
    consulta_insercion = "INSERT INTO prueba (nombre, edad) VALUES (%s, %s)"
    
    # Datos a insertar
    datos_insertar = (a_nombre, a_edad)

    # ejercutar para insertar
    cursor.execute(consulta_insercion, datos_insertar)

    # Confirmar los cambios
    conexion.commit()

    print("Datos insertados correctamente.")

    # Consultar los datos
    cursor.execute("SELECT nombre, edad FROM prueba")
    resultados = cursor.fetchall()

    # Imprimir los resultados
    print("Datos en la tabla después de la inserción:")
    for resultado in resultados:
        nombre, edad = resultado
        print(f"Nombre: {nombre}, Edad: {edad}")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()
