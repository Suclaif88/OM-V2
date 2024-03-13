import mysql.connector
from tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, messagebox
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

# Función para abrir la ventana del administrador
def abrir_ventana_administrador():
    ventana_administrador = Toplevel()
    ventana_administrador.title("Administrador")
    ventana_administrador.configure(bg='#FFD3E0')  # Fondo rosado claro

    # Etiquetas y entradas para ingresar la pregunta y respuestas
    etiqueta_pregunta = Label(ventana_administrador, text="Pregunta:", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_pregunta.grid(row=0, column=0, pady=10, sticky='w')

    entrada_pregunta = Entry(ventana_administrador, width=50)
    entrada_pregunta.grid(row=0, column=1, columnspan=2, pady=10)

    etiquetas_respuestas = []
    entradas_respuestas = []
    for i in range(4):
        etiqueta_respuesta = Label(ventana_administrador, text=f"Respuesta {i + 1}:", font=("Arial", 12), bg='#FFD3E0')
        etiqueta_respuesta.grid(row=i + 1, column=0, pady=5, sticky='w')
        etiquetas_respuestas.append(etiqueta_respuesta)

        entrada_respuesta = Entry(ventana_administrador, width=50)
        entrada_respuesta.grid(row=i + 1, column=1, columnspan=2, pady=5)
        entradas_respuestas.append(entrada_respuesta)

    # Etiquetas y entrada para la respuesta correcta
    etiqueta_correcta = Label(ventana_administrador, text="Respuesta Correcta:", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_correcta.grid(row=5, column=0, pady=10, sticky='w')

    entrada_correcta = Entry(ventana_administrador, width=50)
    entrada_correcta.grid(row=5, column=1, columnspan=2, pady=10)

    # Etiquetas y entrada para el grado
    etiqueta_grado = Label(ventana_administrador, text="Grado (9, 10, 11, Final, Empate):", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_grado.grid(row=6, column=0, pady=10, sticky='w')

    entrada_grado = Entry(ventana_administrador, width=50)
    entrada_grado.grid(row=6, column=1, columnspan=2, pady=10)

    # Función para agregar la pregunta a la base de datos
    def agregar_pregunta():
        pregunta = entrada_pregunta.get()
        respuestas = [entrada_respuesta.get() for entrada_respuesta in entradas_respuestas]
        respuesta_correcta = entrada_correcta.get()
        grado = entrada_grado.get()

        try:
            # Insertar la pregunta y respuestas en la base de datos
            cursor.execute("INSERT INTO preguntas (pregunta, r_1, r_2, r_3, r_4, r_c, grado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (pregunta, respuestas[0], respuestas[1], respuestas[2], respuestas[3], respuesta_correcta, grado))
            conexion.commit()
            messagebox.showinfo("Éxito", "Pregunta agregada exitosamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo agregar la pregunta.\nError: {err}")

   # Botón para agregar la pregunta
    boton_agregar = Button(ventana_administrador, text="Agregar Pregunta", command=agregar_pregunta, bg='#FF69B4', fg='white')
    boton_agregar.grid(row=7, column=0, columnspan=2, pady=10)

# Crear la ventana principal
ventana_principal = Tk()
ventana_principal.title("Olimpiadas de Conocimiento")

# Crear y posicionar los botones en dos columnas
boton_grado_9 = Button(ventana_principal, text='Grado 9°', bg="lightyellow", fg="black", font=('Broadway', 25),
                      width=18, height=3, command=abrir_ventana_preguntas)
boton_grado_10 = Button(ventana_principal, text='Grado 10°', bg="lightblue1", fg="black", font=('Broadway', 25),
                       width=18, height=3, command=abrir_ventana_preguntas)
boton_grado_11 = Button(ventana_principal, text='Grado 11°', bg="lightcoral", fg="black", font=('Broadway', 25),
                       width=18, height=3, command=abrir_ventana_preguntas)
boton_final = Button(ventana_principal, text='Final', bg="lightgreen", fg="black", font=('Broadway', 25),
                    width=18, height=3, command=abrir_ventana_preguntas)
boton_empate = Button(ventana_principal, text='Empate', bg="lightpink", fg="black", font=('Broadway', 25),
                      width=18, height=3, command=abrir_ventana_preguntas)

# Posicionar los botones en dos columnas
boton_grado_9.grid(row=0, column=0, padx=10, pady=10)
boton_grado_10.grid(row=0, column=1, padx=10, pady=10)
boton_grado_11.grid(row=1, column=0, padx=10, pady=10)
boton_final.grid(row=1, column=1, padx=10, pady=10)
boton_empate.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Crear botón de administrador
boton_administrador = Button(ventana_principal, text='Administrador', bg="lightblue", fg="black", font=('Broadway', 25),
                             width=18, height=3, command=abrir_ventana_administrador)
boton_administrador.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Iniciar el bucle principal de la ventana principal
ventana_principal.mainloop()

# Cerrar el cursor y la conexión al cerrar las ventanas
cursor.close()
conexion.close()
