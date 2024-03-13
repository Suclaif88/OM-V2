import mysql.connector
from tkinter import Tk, Label, Button, StringVar, Entry, Toplevel, messagebox, ttk
from random import shuffle

config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'prueba'
}

conexion = mysql.connector.connect(**config)

cursor = conexion.cursor()

ancho_pantalla = 0
alto_pantalla = 0

def obtener_dimensiones_pantalla():
    global ancho_pantalla, alto_pantalla
    root = Tk()
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()
    root.destroy()

obtener_dimensiones_pantalla()

def abrir_ventana_preguntas():
    ventana_preguntas = Toplevel()
    ventana_preguntas.title("Preguntas Aleatorias")
    ventana_preguntas.attributes("-fullscreen", True)
    
    ancho_pantalla = ventana_preguntas.winfo_screenwidth()
    alto_pantalla = ventana_preguntas.winfo_screenheight()

    ventana_preguntas.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana_preguntas.configure(bg='#FFD3E0')

    etiqueta_pregunta = Label(ventana_preguntas, text="", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_pregunta.pack(pady=10)

    etiqueta_respuestas = []
    for i in range(4):
        etiqueta_respuesta = Button(ventana_preguntas, text="", font=("Arial", 10), command=lambda i=i: verificar_respuesta(i))
        etiqueta_respuesta.pack(pady=5)
        etiqueta_respuestas.append(etiqueta_respuesta)

    etiqueta_resultado = Label(ventana_preguntas, text="", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_resultado.pack(pady=10)

    respuesta_correcta = ""
    preguntas_utilizadas = []

    def mostrar_pregunta():
        nonlocal respuesta_correcta
        try:
            cursor.execute("SELECT pregunta, r_1, r_2, r_3, r_4, r_c FROM preguntas")
            preguntas_respuestas = cursor.fetchall()
            preguntas_no_utilizadas = [pregunta for pregunta in preguntas_respuestas if pregunta not in preguntas_utilizadas]
            
            if not preguntas_no_utilizadas:
                etiqueta_pregunta.config(text="Fin del juego")
                for i in range(4):
                    etiqueta_respuestas[i].config(text="")
                etiqueta_resultado.config(text="")
                return

            pregunta_respuesta = preguntas_no_utilizadas[0]
            preguntas_utilizadas.append(pregunta_respuesta)

            pregunta, r_1, r_2, r_3, r_4, r_c = pregunta_respuesta

            opciones_respuesta = [r_1, r_2, r_3, r_4]
            shuffle(opciones_respuesta)

            etiqueta_pregunta.config(text=f"Pregunta: {pregunta}")

            for i in range(4):
                etiqueta_respuestas[i].config(text=opciones_respuesta[i])
            respuesta_correcta = r_c

            etiqueta_resultado.config(text="")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def verificar_respuesta(indice):
        respuesta_usuario = etiqueta_respuestas[indice].cget("text")
        if respuesta_usuario == respuesta_correcta:
            etiqueta_resultado.config(text="Respuesta correcta", fg="green")
        else:
            etiqueta_resultado.config(text=f"Respuesta incorrecta. La correcta es {respuesta_correcta}.", fg="red")

    boton_siguiente = Button(ventana_preguntas, text="Siguiente Pregunta", font=("Arial", 12), command=mostrar_pregunta)
    boton_siguiente.pack(pady=10)

    mostrar_pregunta()

def abrir_ventana_administrador():
    ventana_administrador = Toplevel()
    ventana_administrador.title("Administrador")
    ventana_administrador.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana_administrador.configure(bg='#FFD3E0')

    # Botones para agregar, eliminar y cambiar fondo
    boton_agregar_pregunta = Button(ventana_administrador, text="Agregar Pregunta", command=abrir_ventana_agregar_pregunta, bg='#FF69B4', fg='white')
    boton_agregar_pregunta.pack(pady=10)

    boton_eliminar_preguntas = Button(ventana_administrador, text="Eliminar Preguntas", command=eliminar_preguntas, bg='#FF69B4', fg='white')
    boton_eliminar_preguntas.pack(pady=10)

    boton_cambiar_fondo = Button(ventana_administrador, text="Cambiar Fondo", command=cambiar_fondo, bg='#FF69B4', fg='white')
    boton_cambiar_fondo.pack(pady=10)
    
def abrir_ventana_agregar_pregunta():
    ventana_agregar_pregunta = Toplevel()
    ventana_agregar_pregunta.title("Agregar Pregunta")
    ventana_agregar_pregunta.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana_agregar_pregunta.configure(bg='#FFD3E0')
    
    etiqueta_pregunta = Label(ventana_agregar_pregunta, text="Pregunta:", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_pregunta.grid(row=0, column=0, pady=10, sticky='w')

    entrada_pregunta = Entry(ventana_agregar_pregunta, width=50)
    entrada_pregunta.grid(row=0, column=1, columnspan=2, pady=10)

    etiquetas_respuestas = []
    entradas_respuestas = []
    for i in range(4):
        etiqueta_respuesta = Label(ventana_agregar_pregunta, text=f"Respuesta {i + 1}:", font=("Arial", 12), bg='#FFD3E0')
        etiqueta_respuesta.grid(row=i + 1, column=0, pady=5, sticky='w')
        etiquetas_respuestas.append(etiqueta_respuesta)

        entrada_respuesta = Entry(ventana_agregar_pregunta, width=50)
        entrada_respuesta.grid(row=i + 1, column=1, columnspan=2, pady=5)
        entradas_respuestas.append(entrada_respuesta)

    etiqueta_correcta = Label(ventana_agregar_pregunta, text="Respuesta Correcta:", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_correcta.grid(row=5, column=0, pady=10, sticky='w')

    entrada_correcta = Entry(ventana_agregar_pregunta, width=50)
    entrada_correcta.grid(row=5, column=1, columnspan=2, pady=10)

    etiqueta_grado = Label(ventana_agregar_pregunta, text="Grado (9, 10, 11, Final, Empate):", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_grado.grid(row=6, column=0, pady=10, sticky='w')

    entrada_grado = Entry(ventana_agregar_pregunta, width=50)
    entrada_grado.grid(row=6, column=1, columnspan=2, pady=10)

    def agregar_pregunta():
        pregunta = entrada_pregunta.get()
        respuestas = [entrada_respuesta.get() for entrada_respuesta in entradas_respuestas]
        respuesta_correcta = entrada_correcta.get()
        grado = entrada_grado.get()

        try:
            cursor.execute("INSERT INTO preguntas (pregunta, r_1, r_2, r_3, r_4, r_c, grado) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (pregunta, respuestas[0], respuestas[1], respuestas[2], respuestas[3], respuesta_correcta, grado))
            conexion.commit()
            messagebox.showinfo("Éxito", "Pregunta agregada exitosamente.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo agregar la pregunta.\nError: {err}")

    boton_agregar = Button(ventana_agregar_pregunta, text="Agregar Pregunta", command=agregar_pregunta, bg='#FF69B4', fg='white')
    boton_agregar.grid(row=7, column=0, columnspan=2, pady=10)

def eliminar_preguntas():
    ventana_eliminar_preguntas = Toplevel()
    ventana_eliminar_preguntas.title("Eliminar Preguntas")
    ventana_eliminar_preguntas.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    ventana_eliminar_preguntas.configure(bg='#FFD3E0')

    etiqueta_instrucciones = Label(ventana_eliminar_preguntas, text="Selecciona la pregunta a eliminar:", font=("Arial", 12), bg='#FFD3E0')
    etiqueta_instrucciones.pack(pady=10)

    preguntas_existentes = []

    try:
        cursor.execute("SELECT id, pregunta FROM preguntas")
        preguntas_result = cursor.fetchall()
        for pregunta in preguntas_result:
            id_pregunta, texto_pregunta = pregunta
            preguntas_existentes.append((id_pregunta, texto_pregunta))
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener las preguntas.\nError: {err}")

    pregunta_seleccionada = StringVar()

    opciones_preguntas = [f"{id_pregunta}: {texto_pregunta}" for id_pregunta, texto_pregunta in preguntas_existentes]
    menu_preguntas = ttk.Combobox(ventana_eliminar_preguntas, textvariable=pregunta_seleccionada, values=opciones_preguntas)
    menu_preguntas.pack(pady=10)

    for id_pregunta, texto_pregunta in preguntas_existentes:
        menu_preguntas.insert("end", f"{id_pregunta}: {texto_pregunta}\n")

    def eliminar_pregunta_seleccionada():
        try:
            id_seleccionado = pregunta_seleccionada.get().split(":")[0]

            cursor.execute("DELETE FROM preguntas WHERE id=%s", (id_seleccionado,))
            conexion.commit()

            messagebox.showinfo("Éxito", "Pregunta eliminada exitosamente.")
            ventana_eliminar_preguntas.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo eliminar la pregunta.\nError: {err}")

    boton_eliminar = Button(ventana_eliminar_preguntas, text="Eliminar Pregunta", command=eliminar_pregunta_seleccionada, bg='#FF69B4', fg='white')
    boton_eliminar.pack(pady=10)

def cambiar_fondo():
    # Lógica para cambiar el fondo de la aplicación...
    messagebox.showinfo("Cambiar Fondo", "Funcionalidad en desarrollo.")
    
def salir():
    ventana_principal.destroy()

ventana_principal = Tk()
ventana_principal.title("Olimpiadas de Conocimiento")
ventana_principal.attributes("-fullscreen", True)
ventana_principal.configure(bg="#D0D0D0") 

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
boton_administrador = Button(ventana_principal, text='Administrador', bg="lightblue", fg="black", font=('Broadway', 25),
                             width=18, height=3, command=abrir_ventana_administrador)
boton_salir = Button(ventana_principal, text='SALIR', bg="firebrick1", fg="black", font=('Broadway', 25),
                     width=18, height=3, command=salir)

boton_grado_9.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
boton_grado_10.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
boton_grado_11.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
boton_final.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
boton_empate.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
boton_administrador.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
boton_salir.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

for i in range(4):
    ventana_principal.grid_rowconfigure(i, weight=1)
for i in range(2):
    ventana_principal.grid_columnconfigure(i, weight=1)

ventana_principal.mainloop()

cursor.close()
conexion.close()