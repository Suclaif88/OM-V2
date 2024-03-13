import tkinter as tk
import mysql.connector
from tkinter import Toplevel, Label, Button
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

# Variable global para almacenar la respuesta correcta
respuesta_correcta = ""

def abrir_ventana_preguntas(grado):
    ventana_preguntas = Toplevel()
    ventana_preguntas.title(f"Preguntas Aleatorias - Grado {grado}")

    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_preguntas.winfo_screenwidth()
    alto_pantalla = ventana_preguntas.winfo_screenheight()

    # Definir la geometría de la ventana para ocupar toda la pantalla y color de fondo azul claro
    ventana_preguntas.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana_preguntas.configure(bg='#ADD8E6')  # Fondo azul claro

    # Etiquetas y botones de la ventana de preguntas...
    etiqueta_pregunta = Label(ventana_preguntas, text="", font=("Arial", 12), bg='#ADD8E6')
    etiqueta_pregunta.pack(pady=10)

    etiqueta_respuestas = []
    for i in range(4):
        etiqueta_respuesta = Button(ventana_preguntas, text="", font=("Arial", 10), command=lambda i=i: verificar_respuesta(i))
        etiqueta_respuesta.pack(pady=5)
        etiqueta_respuestas.append(etiqueta_respuesta)

    etiqueta_resultado = Label(ventana_preguntas, text="", font=("Arial", 12), bg='#ADD8E6')
    etiqueta_resultado.pack(pady=10)

    def mostrar_pregunta():
        global respuesta_correcta
        try:
            # Consultar las preguntas y respuestas según el grado
            cursor.execute(f"SELECT pregunta, r_1, r_2, r_3, r_4, r_c FROM preguntas WHERE grado = {grado}")
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

    def verificar_respuesta(indice):
        respuesta_usuario = etiqueta_respuestas[indice].cget("text")
        if respuesta_usuario == respuesta_correcta:
            etiqueta_resultado.config(text="Respuesta correcta", fg="green")
        else:
            etiqueta_resultado.config(text=f"Respuesta incorrecta. La correcta es {respuesta_correcta}.", fg="red")

    # Lista para almacenar preguntas utilizadas
    preguntas_utilizadas = []

    boton_siguiente = Button(ventana_preguntas, text="Siguiente Pregunta", font=("Arial", 12), command=mostrar_pregunta)
    boton_siguiente.pack(pady=10)

    mostrar_pregunta()

# Crear la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Olimpiadas de Conocimiento")  # Título agregado

# Título dentro de la ventana principal
etiqueta_titulo = Label(ventana_principal, text="Olimpiadas de Conocimiento", font=("Arial", 16), pady=10, bg='#ADD8E6')  # Fondo azul claro
etiqueta_titulo.pack()

# Organizar los botones en dos columnas
frame_botones = tk.Frame(ventana_principal, bg='#ADD8E6')  # Fondo azul claro
frame_botones.pack()

boton_grado_9 = Button(frame_botones, text="Grado 9", font=("Arial", 12), command=lambda: abrir_ventana_preguntas(9))
boton_grado_9.grid(row=0, column=0, padx=10, pady=10)

boton_grado_10 = Button(frame_botones, text="Grado 10", font=("Arial", 12), command=lambda: abrir_ventana_preguntas(10))
boton_grado_10.grid(row=0, column=1, padx=10, pady=10)

boton_grado_11 = Button(frame_botones, text="Grado 11", font=("Arial", 12), command=lambda: abrir_ventana_preguntas(11))
boton_grado_11.grid(row=1, column=0, padx=10, pady=10)

boton_final = Button(frame_botones, text="Final", font=("Arial", 12), command=lambda: abrir_ventana_preguntas(1))
boton_final.grid(row=1, column=1, padx=10, pady=10)

boton_empate = Button(frame_botones, text="Empate", font=("Arial", 12), command=lambda: abrir_ventana_preguntas(2))
boton_empate.grid(row=2, column=0, columnspan=2, pady=10)

# Configurar el color de fondo para toda la ventana principal
ventana_principal.configure(bg='#ADD8E6')  # Fondo azul claro

# Centrar la ventana principal en la pantalla
ancho_pantalla_principal = ventana_principal.winfo_screenwidth()
alto_pantalla_principal = ventana_principal.winfo_screenheight()

x_pos = (ancho_pantalla_principal - ventana_principal.winfo_reqwidth()) / 2
y_pos = (alto_pantalla_principal - ventana_principal.winfo_reqheight()) / 2

ventana_principal.geometry(f"+{int(x_pos)}+{int(y_pos)}")

# Iniciar el bucle principal de la ventana principal
ventana_principal.mainloop()

# Cerrar el cursor y la conexión al cerrar las ventanas
cursor.close()
conexion.close()
