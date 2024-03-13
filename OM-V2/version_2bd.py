import mysql.connector
from random import shuffle

# Configuración de la conexión a la base de datos
config = {
    'host': 'localhost',
    'user': 'vale',
    'password': 'Salem31ob',
    'database': 'prueba'
}

# Conectar a la base de datos
conexion = mysql.connector.connect(**config)

# Cursor para ejecutar consultas
cursor = conexion.cursor()

try:
    # Consultar las preguntas y respuestas
    cursor.execute("SELECT pregunta, r_1, r_2, r_3, r_4, r_c FROM preguntas")
    preguntas_respuestas = cursor.fetchall()

    # Organizar las preguntas de forma aleatoria
    shuffle(preguntas_respuestas)

    # Iterar sobre cada pregunta y sus respuestas
    for pregunta_respuesta in preguntas_respuestas:
        pregunta, r_1, r_2, r_3, r_4, r_c = pregunta_respuesta

        # Organizar las opciones de respuesta de forma aleatoria
        opciones_respuesta = [r_1, r_2, r_3, r_4]
        shuffle(opciones_respuesta)

        # Mostrar la pregunta y las respuestas
        print(f"Pregunta: {pregunta}")
        print(f"A: {opciones_respuesta[0]}")
        print(f'B: {opciones_respuesta[1]}')
        print(f'C: {opciones_respuesta[2]}')
        print(f'D: {opciones_respuesta[3]}')

        # Solicitar la respuesta del usuario
        respuesta_usuario = input("Ingrese la letra de la respuesta correcta: ").upper()

        # Verificar la respuesta correcta
        if respuesta_usuario == r_c:
            print("Respuesta correcta.\n")
        else:
            print(f"Respuesta incorrecta. La respuesta correcta es {r_c}.\n")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    conexion.close()
