import mysql.connector
from tkinter import Tk, Label, Button, StringVar, Toplevel
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

def abrir_ventana_preguntas():
    ventana_preguntas = Toplevel()
    ventana_preguntas.title("Preguntas Aleatorias")

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_preguntas.winfo_screenwidth()
    alto_pantalla = ventana_preguntas.winfo_screenheight()

    # Definir la geometría de la ventana para ocupar toda la pantalla
    ventana_preguntas.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana_preguntas.configure(bg='#FFD3E0')  # Fondo rosado claro

    # Etiquetas para mostrar la pregunta y opciones de respuesta
    etiqueta_pregunta = Label(ventana_preguntas, text="", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_pregunta.pack(pady=10)

    etiqueta_respuestas = []
    for i in range(4):
        etiqueta_respuesta = Button(ventana_preguntas, text="", font=("Arial", 10), command=lambda i=i: verificar_respuesta(i))
        etiqueta_respuesta.pack(pady=5)
        etiqueta_respuestas.append(etiqueta_respuesta)

    etiqueta_resultado = Label(ventana_preguntas, text="", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_resultado.pack(pady=10)

    # Variable para almacenar la respuesta correcta
    respuesta_correcta = ""

    # Lista para almacenar preguntas utilizadas
    preguntas_utilizadas = []

    def mostrar_pregunta():
        nonlocal respuesta_correcta
        try:
            # Consultar las preguntas y respuestas
            cursor.execute("SELECT pregunta, r_1, r_2, r_3, r_4, r_c FROM preguntas")
            preguntas_respuestas = cursor.fetchall()

            # Organizar las preguntas de forma aleatoria
            preguntas_no_utilizadas = [pregunta for pregunta in preguntas_respuestas if pregunta not in preguntas_utilizadas]
            
            if not preguntas_no_utilizadas:
                # Si no quedan preguntas no utilizadas, mostrar fin del juego
                etiqueta_pregunta.config(text="Fin del juego")
                for i in range(4):
                    etiqueta_respuestas[i].config(text="")
                etiqueta_resultado.config(text="")
                return

            pregunta_respuesta = preguntas_no_utilizadas[0]
            preguntas_utilizadas.append(pregunta_respuesta)

            pregunta, r_1, r_2, r_3, r_4, r_c = pregunta_respuesta

            # Organizar las opciones de respuesta de forma aleatoria
            opciones_respuesta = [r_1, r_2, r_3, r_4]
            shuffle(opciones_respuesta)

            # Mostrar la pregunta y las respuestas
            etiqueta_pregunta.config(text=f"Pregunta: {pregunta}")

            for i in range(4):
                etiqueta_respuestas[i].config(text=opciones_respuesta[i])

            # Almacenar la respuesta correcta
            respuesta_correcta = r_c

            # Limpiar la etiqueta de resultado
            etiqueta_resultado.config(text="")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # Función para verificar la respuesta
    def verificar_respuesta(indice):
        respuesta_usuario = etiqueta_respuestas[indice].cget("text")
        if respuesta_usuario == respuesta_correcta:
            etiqueta_resultado.config(text="Respuesta correcta", fg="green")
        else:
            etiqueta_resultado.config(text=f"Respuesta incorrecta. La correcta es {respuesta_correcta}.", fg="red")

    # Botón para mostrar la siguiente pregunta
    boton_siguiente = Button(ventana_preguntas, text="Siguiente Pregunta", font=("Arial", 12), command=mostrar_pregunta)
    boton_siguiente.pack(pady=10)

    # Mostrar la primera pregunta al inicio
    mostrar_pregunta()

# Crear la ventana principal
ventana_principal = Tk()
ventana_principal.title("Ventana Principal")

# Botón para abrir la ventana de preguntas
boton_preguntas = Button(ventana_principal, text="Preguntas", font=("Arial", 12), command=abrir_ventana_preguntas)
boton_preguntas.pack(pady=50)

# Iniciar el bucle principal de la ventana principal
ventana_principal.mainloop()

# Cerrar el cursor y la conexión al cerrar las ventanas
cursor.close()
conexion.close()
