import tkinter as tk
from tkinter import messagebox
import json
import sys
import os
from PIL import Image, ImageTk
import pymysql
import re
from plyer import notification
import tkinter.filedialog as filedialog

Usuario_actual = None
contraseña_actual = None
Correo_actual = None

idioma_actual = "es"
bg_actual = "white"
bg_gris="#dddddd"


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

SESSION_FILE = "data/account.json"

def guardar_sesion(correo, nombre):
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)  #Crea el archivo account si no existe en  la carpeta data
    with open(SESSION_FILE, "w") as f:
        json.dump({"Correo": correo, "Nombre": nombre}, f)

def cargar_sesion():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return json.load(f)
    return None

def Cerrar_sesion():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
    global Usuario_actual, Correo_actual
    Usuario_actual, Correo_actual = None, None
    messagebox.showinfo(textos["cerrar_sesion"], textos["sesion_cerrada"])
    actualizar_interfaz()

def cargar_lenguaje(archivo):
    ruta_relativa = os.path.join("Languages", archivo)
    if not os.path.exists(ruta_relativa):
        raise FileNotFoundError(f"El archivo de lenguaje '{ruta_relativa}' no existe.")
    with open(ruta_relativa, "r", encoding="utf-8") as f:
        return json.load(f)

def cambiar_lenguaje(lenguaje):
    global textos,idioma_actual
    if lenguaje == "es":
        textos = cargar_lenguaje("es.json")
        idioma_actual = "es"

    elif lenguaje == "en":
        textos = cargar_lenguaje("en.json")
        idioma_actual = "en"

    elif lenguaje =="fr":
        textos = cargar_lenguaje("fr.json")
        idioma_actual = "fr"

    elif lenguaje == "pt":
        textos = cargar_lenguaje("pt.json")
        idioma_actual = "pt"

    elif lenguaje == "he":
        textos = cargar_lenguaje("he.json")
        idioma_actual = "he"
    

    actualizar_interfaz()

def actualizar_interfaz():
    Limpiar_Frame()
    Mostrar_barra_lateral()
    global Frame_titulo
    Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
    Frame_titulo.place(x=200, y=0, height=99, width=800)


    logo_path = resource_path("images/Logo.png")

    imagen = Image.open(logo_path)
    imagen = imagen.resize((90, 90), Image.LANCZOS)
    
    imagen_logo = ImageTk.PhotoImage(imagen) 

    lbl_logo = tk.Label(Frame, image=imagen_logo, bg=bg_actual)
    lbl_logo.pack(anchor="se")

    Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
    Frame_titulo.place(x=200, y=0, height=99, width=800)
    lbl_titulo = tk.Label(Frame_titulo, text=textos["titulo_principal"], bg=bg_gris, fg="#007BFF", font=("Arial", 36, "bold"))
    lbl_titulo.place(x=10, y=10)

    btn_ver_actividades = tk.Button(Frame, text=textos["ver_actividades"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,
                                    command=verActividades)
    btn_ver_actividades.place(x=0, y=100, height=60, width=200)

    btn_gestionar_tareas = tk.Button(Frame, text=textos["gestionar_tareas"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,
                                     command=gestionarTareas)
    btn_gestionar_tareas.place(x=0, y=170, height=60, width=200)

    lbl_separador = tk.Label(Frame, text="____________", font=("Arial", 20), bg="#007BFF", fg=bg_actual)
    lbl_separador.place(x=7, y=280)

    btn_configuración = tk.Button(Frame, text=textos["configuracion"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0, command=Ver_Configuraciones)
    btn_configuración.place(x=0, y=380, height=60, width=200)

    btn_cuenta = tk.Button(Frame, text=textos["cuenta"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0, command=Ver_Cuenta)
    btn_cuenta.place(x=0, y=450, height=60, width=200)

    btn_acerca_de = tk.Button(Frame, text=textos["acerca_de"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,command=Ver_acerca_de)
    btn_acerca_de.place(x=0, y=520, height=60, width=200)



def Limpiar_Frame():
    for widget in Frame.winfo_children():
        widget.place_forget()

def Ver_Configuraciones():
    Limpiar_Frame()
    Mostrar_barra_lateral()
    global Frame_titulo, btn_configuracion_de_la_cuenta, btn_configuracion_notificaciones,lbl_titulo1
    global btn_configuracion_elegir_tema, btn_configuracion_lenguaje,btn_acerca_de

    Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
    Frame_titulo.place(x=200, y=0, height=99, width=800)
    lbl_titulo2 = tk.Label(Frame_titulo, text=textos["configuracion"], bg=bg_gris, fg="#007BFF", font=("Arial", 36, "bold"))
    lbl_titulo2.place(x=10, y=20)


    btn_configuracion_de_la_cuenta = tk.Button(Frame, text=textos["configuracion_de_la_cuenta"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1,
                                               command=Ver_cuenta_con_sesion_iniciada)
    btn_configuracion_de_la_cuenta.place(x=200, y=99, height=99, width=805)

    btn_configuracion_notificaciones = tk.Button(Frame, text=textos["notificaciones"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1,
                                                 command=verNotificaciones)
    btn_configuracion_notificaciones.place(x=200, y=199, height=99, width=805)

    btn_configuracion_elegir_tema = tk.Button(Frame, text=textos["elegir_tema"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1,command=elegir_tema)
    btn_configuracion_elegir_tema.place(x=200, y=299, height=99, width=805)

    btn_configuracion_lenguaje = tk.Button(Frame, text=textos["lenguaje"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1, command=Elegir_lenguaje)
    btn_configuracion_lenguaje.place(x=200, y=399, height=99, width=805)

#
#
#
#
#
def verTareas(id_clase):
    try:
        query = "SELECT * FROM tareas_cursas WHERE ID_clase = %s"
        cursor.execute(query, (id_clase,))
        tareas = cursor.fetchall()

        for widget in ventanaGes.winfo_children():
            widget.destroy()

        labelTareas = tk.Label(
            ventanaGes,
            text="Tareas de la clase",
            font=("Cascadia code", 20),
            background=bg_actual,
            foreground="#007BFF"
        )
        labelTareas.pack(pady=15, side=tk.TOP, anchor="nw", padx=25)

        for tarea in tareas:
            nombre_tarea = tarea[1]  #Nombre de la tarea
            tema_tarea = tarea[2]  #Tema de la tarea
            tarea_id = tarea[0]  #ID de la tarea

            tarea_btn = tk.Button(
                ventanaGes,
                text=f"{nombre_tarea}: {tema_tarea}",
                width=60,
                height=3,
                bg=bg_gris,
                fg="#007BFF",
                font=("Cascadia code", 9),
                command=lambda tarea_id=tarea_id: descargar_pdf(tarea_id)
            )
            tarea_btn.pack(padx=25, pady=10)

            btn_entregada = tk.Button(
                ventanaGes,
                text="Marcar como entregada",
                bg="#28a745",
                fg="white",
                font=("Cascadia code", 9),
                command=lambda tarea_id=tarea_id: marcar_tarea_entregada(tarea_id, id_clase) 
            )
            btn_entregada.pack(padx=25, pady=10)

        btn_progreso = tk.Button(
            ventanaGes,
            text=textos["ver_progreso"],
            bg="#007BFF",  
            fg="white",
            font=("Arial", 12),
            command=lambda: calcular_progreso(id_clase)  
        )
        btn_progreso.pack(pady=10)

    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error al obtener las tareas: {e}")

def verTareasImpartidas(id_clase):
    try:
        query = "SELECT * FROM tareas_cursas WHERE ID_clase = %s"
        cursor.execute(query, (id_clase,))
        tareas = cursor.fetchall()

        for widget in ventanaGes.winfo_children():
            widget.destroy()

        def PublicarTarea():
            nombre_tarea = entryNombreTarea.get().strip()
            tema_tarea = entryTemaTarea.get().strip()

            if not nombre_tarea or not tema_tarea:
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            # Seleccionar archivo PDF
            archivo_pdf = filedialog.askopenfilename(
                title="Seleccionar archivo PDF",
                filetypes=[("Archivos PDF", "*.pdf")]
            )

            if not archivo_pdf:
                messagebox.showerror("Error", "Debe seleccionar un archivo PDF.")
                return

            try:
                # Leer el archivo PDF
                with open(archivo_pdf, 'rb') as file:
                    archivo_blob = file.read()

                # Guardar en la base de datos
                query = "INSERT INTO tareas_cursas (Nombre, Tema, ID_clase, Archivo) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (nombre_tarea, tema_tarea, id_clase, archivo_blob))
                conexion.commit()
                messagebox.showinfo("Éxito", "Tarea publicada correctamente.")
                verTareasImpartidas(id_clase)

            except pymysql.Error as e:
                messagebox.showerror("Error", f"No se pudo publicar la tarea: {e}")

        # Interfaz para agregar tarea
        labelAgregarTarea = tk.Label(Frame_titulo, text="Agregar Nueva Tarea", font=("Cascadia code", 14), background=bg_gris, foreground="#007BFF")
        labelAgregarTarea.place(relx=0.55, rely=0.1, y=-20)

        tk.Label(Frame_titulo, text="Nombre de la tarea ", width=20, bg=bg_gris, foreground="#007BFF", font=("Cascadia code", 12)).place(relx=0.5, rely=0.2, x=-20)
        entryNombreTarea = tk.Entry(Frame_titulo, width=15, font=("Arial", 12), foreground="white", relief="flat", bg="#007BFF", fg="white")
        entryNombreTarea.place(relx=0.5, rely=0.5)

        tk.Label(Frame_titulo, text="Tema de la tarea ", width=20, bg=bg_gris, foreground="#007BFF", font=("Cascadia code", 12)).place(relx=0.7, rely=0.2, x=-20)
        entryTemaTarea = tk.Entry(Frame_titulo, width=15, font=("Arial", 12), foreground="white", relief="flat", bg="#007BFF", fg="white")
        entryTemaTarea.place(relx=0.7, rely=0.5)

        botonPublicarTarea = tk.Button(Frame_titulo, text="Publicar Tarea", bg="#007BFF", fg="white", font=("Arial", 8), command=PublicarTarea)
        botonPublicarTarea.place(rely=0.6, relx=0.9, y=-10)

        # Mostrar tareas existentes con botones
        for tarea in tareas:
            nombre_tarea = tarea[1]
            tema_tarea = tarea[2]

            tarea_btn = tk.Button(
                ventanaGes,
                text=f"{nombre_tarea}\n{tema_tarea}",
                width=60,
                height=3,
                fg="#007BFF",
                bg=bg_gris,
                font=("Cascadia code", 15),
                command=lambda tarea_id=tarea[0]: descargar_pdf(tarea_id)
            )
            tarea_btn.pack(padx=25, pady=10)

    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error al obtener las tareas: {e}")

# Descargar el PDF de la base de datos
def descargar_pdf(tarea_id):
    try:
        query = "SELECT Archivo FROM tareas_cursas WHERE ID = %s"
        cursor.execute(query, (tarea_id,))
        resultado = cursor.fetchone()

        if resultado and resultado[0]:
            archivo_pdf = filedialog.asksaveasfilename(
                title="Guardar archivo PDF",
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")]
            )

            if archivo_pdf:
                with open(archivo_pdf, 'wb') as file:
                    file.write(resultado[0])

                messagebox.showinfo("Éxito", "Archivo descargado correctamente.")
        else:
            messagebox.showerror("Error", "No se encontró ningún archivo asociado a esta tarea.")

    except pymysql.Error as e:
        messagebox.showerror("Error", f"No se pudo descargar el archivo: {e}")
#
#
#
#
def Ver_Cuenta():
    global  lbl_contraseña,lbl_email,lbl_nombre,btn_iniciar_sesion,entry_nombre,entry_contraseña,entry_email
    global btn_registrarse,btn_cambiar_contraseña
    Limpiar_Frame()
    Mostrar_barra_lateral()

    if Usuario_actual == None:

        Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
        Frame_titulo.place(x=200, y=0, height=99, width=800)
        lbl_titulo2 = tk.Label(Frame_titulo, text=textos["cuenta"], bg=bg_gris, fg="#007BFF", font=("Arial", 36, "bold"))
        lbl_titulo2.place(x=10, y=20)

        image_path = resource_path("images/imagen_login.png")
        imagen = Image.open(image_path)
        imagen = imagen.resize((100, 100), Image.LANCZOS)
        imagen_tk = ImageTk.PhotoImage(imagen)
        lbl_imagen = tk.Label(Frame, image=imagen_tk, bg=bg_actual)
        lbl_imagen.image = imagen_tk
        lbl_imagen.place(x=550, y=150)

        lbl_nombre = tk.Label(Frame, text=textos["nombre"], font=("Arial", 12), bg=bg_actual,fg="#007BFF")
        lbl_nombre.place(x=370, y=280)
        entry_nombre = tk.Entry(Frame, bd=1, font=("Arial", 14), relief="flat", bg="#007BFF",fg=bg_actual)
        entry_nombre.place(x=370, y=310, width=410, height=30)

        lbl_email = tk.Label(Frame, text=textos["email"], font=("Arial", 12), bg=bg_actual,fg="#007BFF")
        lbl_email.place(x=370, y=360)
        entry_email = tk.Entry(Frame, bd=1, font=("Arial", 14), relief="flat", bg="#007BFF",fg=bg_actual)
        entry_email.place(x=370, y=390, width=410, height=30)

        lbl_contraseña = tk.Label(Frame, text=textos["contraseña"], font=("Arial", 12), bg=bg_actual,fg="#007BFF")
        lbl_contraseña.place(x=370, y=440)
        entry_contraseña = tk.Entry(Frame, bd=1, font=("Arial", 14), relief="flat", bg="#007BFF",fg=bg_actual, show="*")
        entry_contraseña.place(x=370, y=470, width=410, height=30)

        btn_iniciar_sesion = tk.Button(Frame, text=textos["iniciar_sesion"], bg="#007BFF",fg=bg_actual,
                                        font=("Arial", 14), relief="flat",command=Iniciar_sesion)
        btn_iniciar_sesion.place(x=370, y=520, width=200, height=40)

        btn_registrarse = tk.Button(Frame, text=textos["registrarse"], bg="#007BFF",fg=bg_actual,
                                        font=("Arial", 14), relief="flat",command=mostrar_registrarse)
        btn_registrarse.place(x=580, y=520, width=200, height=40)
    else:
        Ver_cuenta_con_sesion_iniciada()

def verificar_sesion_activa():
    sesion = cargar_sesion()
    if sesion:
        global Usuario_actual, Correo_actual
        Usuario_actual = sesion["Nombre"]
        Correo_actual = sesion["Correo"]
        print(f"Sesión cargada: Usuario={Usuario_actual}, Correo={Correo_actual}")  # Depuración
        messagebox.showinfo(textos["bienvenido"], textos["bienvenido_de_nuevo"] + ", " + Usuario_actual)
        Mostrar_barra_lateral()
    else:
        actualizar_interfaz()

def Iniciar_sesion():
    global Usuario_actual, Correo_actual

    nombre = entry_nombre.get()
    correo = entry_email.get()
    contraseña = entry_contraseña.get()

    try:
        query = "SELECT * FROM usuarios WHERE Correo = %s AND Nombre = %s AND Contraseña = %s"
        cursor.execute(query, (correo, nombre, contraseña))
        resultado = cursor.fetchone()

        if resultado:
            Usuario_actual, Correo_actual = nombre, correo
            guardar_sesion(correo, nombre)
            messagebox.showinfo(textos["inicio_de_sesion"], textos["inicio_de_sesion_exitoso"])
            Limpiar_Frame()
            Mostrar_barra_lateral()
        else:
            messagebox.showerror(textos["error"], textos["credenciales_incorrectas"])
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

def mostrar_registrarse():
    Ver_Cuenta()
    btn_iniciar_sesion.place_forget()
    btn_registrarse.place(x=490)
    btn_registrarse.config(command=registrarse)

def registrarse():
    nombre = entry_nombre.get()
    correo = entry_email.get()
    contraseña = entry_contraseña.get()

    if not correo or not nombre or not contraseña:
        messagebox.showerror(textos["error"],textos["ningun_campo_debe_estar_vacio"])
    else:
        if not correo.endswith("@gmail.com"):
            messagebox.showerror(textos["error"],textos[ "correo_no_valido"])
        else:
            if len(contraseña) < 8:
                messagebox.showerror(textos["error"],textos[ "numero_de_c_de_contraseña"])
            else:
                if not re.search(r'[A-Za-z]', contraseña) or not re.search(r'[0-9]', contraseña):
                    messagebox.showerror(textos["error"], textos["letras_de_contraseña"])
                else:
                    query = "Select * from usuarios where Correo = %s"
                    cursor.execute(query,(correo,))
                    resultado = cursor.fetchone()
                    if not resultado:
                        global Usuario_actual, Correo_actual
                        guardar_sesion(correo, nombre)
                        messagebox.showinfo(textos["exito"],textos[ "registro_exitoso"])
                        cursor.execute("Insert into usuarios (Correo,Nombre,Contraseña) Values(%s,%s,%s)",(correo,nombre,contraseña))
                        Usuario_actual,Correo_actual = nombre, correo
                        Limpiar_Frame()
                        Mostrar_barra_lateral()
                        conexion.commit()
                    else:
                        messagebox.showerror(textos["error"],textos["correo_ya_registrado"])
                    
def Elegir_lenguaje():
    Limpiar_Frame()
    Mostrar_barra_lateral()

    Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
    Frame_titulo.place(x=200, y=0, height=99, width=800)
    lbl_titulo2 = tk.Label(Frame_titulo, text=textos["configuracion"], bg=bg_gris, fg="#007BFF", font=("Arial", 36, "bold"))
    lbl_titulo2.place(x=10, y=20)

    idioma_seleccionado = tk.StringVar(value=idioma_actual) 

    def seleccionar_idioma_actual():
        cambiar_lenguaje(idioma_seleccionado.get())

    rb_idioma_español = tk.Radiobutton(Frame,bg=bg_actual, fg="#007BFF", text=textos["idioma_español"], variable=idioma_seleccionado, value="es", command=seleccionar_idioma_actual, font=("Arial", 20))
    rb_idioma_ingles = tk.Radiobutton(Frame,bg=bg_actual, fg="#007BFF", text=textos["idioma_ingles"], variable=idioma_seleccionado, value="en", command=seleccionar_idioma_actual, font=("Arial", 20))
    rb_idioma_frances = tk.Radiobutton(Frame, bg=bg_actual, fg="#007BFF",text=textos["idioma_frances"], variable=idioma_seleccionado, value="fr", command=seleccionar_idioma_actual, font=("Arial", 20))
    rb_idioma_portugues = tk.Radiobutton(Frame,bg=bg_actual,  fg="#007BFF",text=textos["idioma_portugues"], variable=idioma_seleccionado, value="pt", command=seleccionar_idioma_actual, font=("Arial", 20))
    rb_idioma_hebreo = tk.Radiobutton(Frame, bg=bg_actual, fg="#007BFF",text=textos["idioma_hebreo"], variable=idioma_seleccionado, value="he", command=seleccionar_idioma_actual, font=("Arial", 20))

    rb_idioma_español.place(x=210, y=100,height=100,width=200)
    rb_idioma_ingles.place(x=210, y=200,height=100,width=200)
    rb_idioma_frances.place(x=210, y=300,height=100,width=200)
    rb_idioma_portugues.place(x=210, y=400,height=100,width=200)
    rb_idioma_hebreo.place(x=210, y=500,height=100,width=200)
def elegir_tema():
    Limpiar_Frame()
    Mostrar_barra_lateral()

    def cambiar_tema(tema,titulo):
        global bg_actual,bg_gris
        bg_actual = tema
        bg_gris=titulo
        Frame.config(bg=bg_actual)
        Frame_titulo.config(bg=bg_gris)

        rb_tema_claro.config(bg=bg_actual)
        rb_tema_oscuro.config(bg=bg_actual)
        lbl_logo.config(bg=bg_actual)
        Mostrar_barra_lateral()


    tema_seleccionado = tk.StringVar(value=bg_actual)
    rb_tema_claro = tk.Radiobutton(Frame, bg=bg_actual, fg="#007BFF", text=textos["tema_claro"], variable=tema_seleccionado, value="white", command=lambda: cambiar_tema("white","#dddddd"), font=("Arial", 20))
    rb_tema_oscuro = tk.Radiobutton(Frame, bg=bg_actual,  fg="#007BFF",text=textos["tema_oscuro"], variable=tema_seleccionado, value="black", command=lambda: cambiar_tema("black","#363636"), font=("Arial", 20))

    rb_tema_claro.place(x=210, y=100,height=100,width=200)
    rb_tema_oscuro.place(x=210, y=200,height=100,width=200)

def Mostrar_barra_lateral():


    Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
    Frame_titulo.place(x=200, y=0, height=99, width=800)
    lbl_titulo1 = tk.Label(Frame_titulo, text=textos["titulo_principal"], bg=bg_gris, fg="#007BFF", font=("Arial", 36, "bold"))
    lbl_titulo1.place(x=10, y=10)

    Frame_barra_lateral = tk.Frame(Frame, bg="#007BFF").place(x=0, y=0, height=600, width=200)

    lbl_titulo = tk.Label(Frame_barra_lateral, text=textos["titulo_principal"], font=("Arial", 24), bg="#007BFF", fg=bg_actual)
    lbl_titulo.place(x=25, y=10)

    btn_ver_actividades = tk.Button(Frame_barra_lateral, text=textos["ver_actividades"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,
                                    command=verActividades)
    btn_ver_actividades.place(x=0, y=100, height=60, width=200)

    btn_gestionar_tareas = tk.Button(Frame_barra_lateral, text=textos["gestionar_tareas"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,
                                     command=gestionarTareas)
    btn_gestionar_tareas.place(x=0, y=170, height=60, width=200)


    lbl_separador = tk.Label(Frame_barra_lateral, text="____________", font=("Arial", 20), bg="#007BFF", fg=bg_actual)
    lbl_separador.place(x=7, y=280)

    btn_configuración = tk.Button(Frame_barra_lateral, text=textos["configuracion"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0, command=Ver_Configuraciones)
    btn_configuración.place(x=0, y=380, height=60, width=200)

    btn_cuenta = tk.Button(Frame_barra_lateral, text=textos["cuenta"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,
                           command=Ver_Cuenta)
    btn_cuenta.place(x=0, y=450, height=60, width=200)

    btn_acerca_de = tk.Button(Frame_barra_lateral, text=textos["acerca_de"], bg="#007BFF", fg=bg_actual, font=("Arial", 15), bd=0,command=Ver_acerca_de)
    btn_acerca_de.place(x=0, y=520, height=60, width=200)

def verActividades():
    global Frame_titulo,entry_nombre_de_la_clase,lbl_nombre_de_la_clase,btn_publicar_clase,lbl_titulo
    defecto=textos["buscar_clase"]

    def scroll_canvas(event, canvas):
        if event.delta: 
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        else: 
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def on_focus_in(event):
        if entry_buscar.get() == defecto:
            entry_buscar.delete(0, tk.END)  
            entry_buscar.config(fg='white')  
    def on_focus_out(event):
        if entry_buscar.get() == '':
            entry_buscar.insert(0, defecto)  
            entry_buscar.config(fg='White')

    def ver_agregarClase():
        global entry_nombre_de_la_clase
        if Usuario_actual == None:
            messagebox.showwarning(textos["atencion"],textos["sin_cuenta"])
        else:
            actualizar_interfaz()

            lbl_nombre_de_la_clase = tk.Label(Frame, text=textos["nombre_de_la_clase"], font=("Arial", 12), bg=bg_actual,fg="#007BFF")
            lbl_nombre_de_la_clase.place(x=370, y=140)
            entry_nombre_de_la_clase = tk.Entry(Frame, bd=1, font=("Arial", 14), relief="flat", bg="#007BFF",fg=bg_actual)
            entry_nombre_de_la_clase.place(x=370, y=170, width=410, height=30)

            btn_publicar_clase = tk.Button(Frame, )
            btn_publicar_clase = tk.Button(Frame, text=textos["publicar_clase"], bg="#007BFF",fg=bg_actual,
                                    font=("Arial", 14), relief="flat",command=agregar_clase)
            btn_publicar_clase.place(x=370, y=220, width=200, height=40)


            nuevoFrame= tk.Frame(ventanaCLa,width=700,height=100,bg=bg_gris)
            nuevoFrame.pack(padx=25,pady=10)

            ventanaCLa.update_idletasks()
            canva.config(scrollregion=canva.bbox("all"))
    def unirse_a_clase(id_clase, nombre_clase):
        global Usuario_actual, Correo_actual
        print(f"Intentando unirse a clase: ID={id_clase}, Nombre={nombre_clase}")
        if Usuario_actual is None or Correo_actual is None:
            messagebox.showwarning("Atención", "Debe iniciar sesión para unirse a una clase.")
            return
        try:
            query_verificar = "SELECT * FROM estudiantes_clases WHERE ID_Clase = %s AND Correo_Estudiante = %s"
            cursor.execute(query_verificar, (id_clase, Correo_actual))
            if cursor.fetchone():
                messagebox.showinfo("Información", f"Ya está inscrito en la clase '{nombre_clase}'.")
                return
            
            query_insertar = "INSERT INTO estudiantes_clases (ID_Clase, Correo_Estudiante, Nombre_Clase) VALUES (%s, %s, %s)"
            cursor.execute(query_insertar, (id_clase, Correo_actual, nombre_clase))
            conexion.commit()
            messagebox.showinfo("Éxito", f"Se ha unido exitosamente a la clase '{nombre_clase}'.")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"Error al unirse a la clase: {e}")


    def agregar_clase():
        global entry_nombre_de_la_clase, Correo_actual
        try:
            nombre_de_la_clase = entry_nombre_de_la_clase.get()

            cursor.execute("Insert into clases(Nombre,Docente,Correo_Docente) Values(%s,%s,%s)",(nombre_de_la_clase,Usuario_actual,Correo_actual))
            conexion.commit()
            messagebox.showinfo(textos["publicacion"],textos["clase_publicada"])
        except pymysql.Error as e:
            messagebox.showerror(textos["error"],e)

    actualizar_interfaz()

    canva = tk.Canvas(Frame, height=500, width=795, background=bg_actual) 
    canva.place(relx=0.3, rely=0.2, x=-100, y=-23)

    ventanaCLa = tk.Frame(canva, bg="lightgray")

    canva.create_window((0, 0), window=ventanaCLa, anchor="nw")  

    ventanaCLa.config(background=bg_actual)
    cursor.execute("select * from clases")
    clases = cursor.fetchall()

    canva.bind_all("<MouseWheel>", lambda event, canvas=canva: scroll_canvas(event, canvas))

    for clase in clases:
        id_clase, nombre_clase, docente_clase, correo_docente = clase
        clase_frame = tk.Button(
            ventanaCLa,
            width=30,
            height=2,
            text=nombre_clase,
            font=("Arial", 34),
            bg=bg_gris,
            bd=0,
            command=lambda id_clase=id_clase, nombre_clase=nombre_clase: unirse_a_clase(id_clase, nombre_clase)
        )
        clase_frame.pack(padx=10, pady=10)



    ventanaCLa.update_idletasks()  
    canva.config(scrollregion=canva.bbox("all")) 

    scrollbar = tk.Scrollbar(Frame, orient="vertical", command=canva.yview,troughcolor="red")
    scrollbar.place(x=985, y=99, height=500)  

    canva.configure(yscrollcommand=scrollbar.set)

    entry_buscar=tk.Entry(Frame_titulo,width=25,justify="center",bg="#007BFF",bd=0,font=("Arial",15), foreground="white")
    entry_buscar.place(relx=0.35,rely=0.5,x=50,y=3)
    entry_buscar.insert(0,defecto)
    entry_buscar.bind("<FocusOut>", on_focus_out)
    entry_buscar.bind("<FocusIn>", on_focus_in) 


    crear_clase = tk.Button(Frame_titulo,text=textos["buscar_clase"],bg=bg_gris,fg="#007BFF",
              bd=1).place(relx=0.8,rely=0.5,y=3)
    buscar_clase = tk.Button(Frame_titulo,text=textos["crear_clase"],bg=bg_gris,fg="#007BFF",command=ver_agregarClase,
              bd=1).place(relx=0.9,rely=0.5,y=3)

def gestionarTareas():
    global ventanaGes
    actualizar_interfaz()

    def scroll_canvas(event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canva = tk.Canvas(Frame, height=500, width=795, background=bg_actual)
    canva.place(relx=0.3, rely=0.2, x=-100, y=-23)

    ventanaGes = tk.Frame(canva, bg="lightgray")
    canva.create_window((0, 0), window=ventanaGes, anchor="nw")
    ventanaGes.config(background=bg_actual)

    labelClasesImp = tk.Label(
        ventanaGes,
        text="Clases que impartes",
        font=("Cascadia code", 20),
        background=bg_actual,
        foreground="#007BFF"
    )
    labelClasesImp.pack(pady=15, side=tk.TOP, anchor="nw", padx=25)
#CLASES QUE IMPARTE
    
    try:
        query = "SELECT * FROM clases WHERE Correo_Docente = %s"
        cursor.execute(query, (Correo_actual,))
        resultados = cursor.fetchall()

        for resultado in resultados:
            nombre_clase = resultado[1]  #índice 1 es el la columna "Nombre" en la tabla de clases
            id_clase=resultado[0]


            frame = tk.Button(ventanaGes, width=100, height=6, background=bg_gris, bd=0,text=nombre_clase,fg="#007BFF",command=lambda id_clase=id_clase: verTareasImpartidas(id_clase))
            frame.pack(padx=25, pady=10)

    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error al obtener las clases: {e}")
        print(e)

    labelClasesrec = tk.Label(
        ventanaGes,
        text="Clases que cursas",
        font=("Cascadia code", 20),
        background=bg_actual,
        foreground="#007BFF"
    )


#
#
#
#
#
#
#
#

    labelClasesrec.pack(pady=15, side=tk.TOP, anchor="nw", padx=25)
#CLASES QUE CURSA
    try:
        query1 = "Select * from estudiantes_clases where Correo_Estudiante = %s"
        cursor.execute(query1,(Correo_actual,))
        resultados1 = cursor.fetchall()

        for resultado1 in resultados1:
            nombre_clase1 = resultado1[3]
            id_clase=resultado1[1]
        
            frame = tk.Button(ventanaGes, width=100, height=6, background=bg_gris, bd=0,text=nombre_clase1,fg="#007BFF",font=("Cascadia code",9),command=lambda id_clase=id_clase: verTareas(id_clase))
            frame.pack(padx=25, pady=10)


    except pymysql.Error as e:
        messagebox.showerror(textos["error"],e)
        

    ventanaGes.update_idletasks()
    canva.config(scrollregion=canva.bbox("all"))

    scrollbar = tk.Scrollbar(Frame, orient="vertical", command=canva.yview, troughcolor="red")
    scrollbar.place(x=985, y=99, height=500)

    canva.configure(yscrollcommand=scrollbar.set)
    canva.bind_all("<MouseWheel>", lambda event, canvas=canva: scroll_canvas(event, canvas))
#
#
#
#
#
#
def verNotificaciones():
    actualizar_interfaz()
    def scroll_canvas(event, canvas):
        if event.delta: 
            canvas.yview_scroll(-1 * (event.delta // 120), "units")
        else: 
            canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def notificacion():
        if var.get()== 1:
            notification.notify(
                title="AcadeMix",
                message="Tienes un mensaje ",
                timeout=1
            )
        else:
            notification.notify(
                title="AcadeMix",
                message="No resiviras notificaciones jsjsjsj 🤣 ",
                timeout=1
            )
    canva = tk.Canvas(Frame, height=500, width=795, background=bg_actual)
    canva.place(relx=0.3, rely=0.2, x=-100, y=-23)
    ventanaNoti = tk.Frame(canva, bg="lightgray")

    canva.create_window((0, 0), window=ventanaNoti, anchor="nw")  

    ventanaNoti.config(background=bg_actual)

    var=tk.IntVar()
    si_rdtk=tk.Radiobutton(ventanaNoti,text=textos["si"],variable=var, value="1",background=bg_actual,width=3,font=("Arial",15),height=2,foreground="#007BFF",command=notificacion)
    no_rdtk=tk.Radiobutton(ventanaNoti,text=textos["no"],variable=var, value="2",background=bg_actual,width=3,font=("Arial",15),height=2,foreground="#007BFF",command=notificacion)

    tk.Label(ventanaNoti,text=textos["desea_recibir_notificaciones"],font=("Arial",20),bg=bg_actual,foreground="#007BFF").pack()
    si_rdtk.pack()
    no_rdtk.pack()

    ventanaNoti.update_idletasks()  
    canva.config(scrollregion=canva.bbox("all")) 

    scrollbar = tk.Scrollbar(Frame, orient="vertical", command=canva.yview,troughcolor="red")
    scrollbar.place(x=985, y=99, height=500)  

    canva.configure(yscrollcommand=scrollbar.set)
    canva.bind_all("<MouseWheel>", lambda event, canvas=canva: scroll_canvas(event, canvas))
def Ver_cuenta_con_sesion_iniciada():

    if Usuario_actual != None:

        btn_cambiar_contraseña = tk.Button(Frame, text=textos["cambiar_contraseña"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1,
                                                                    command=Cambiar_contraseña)
        btn_cambiar_contraseña.place(x=200, y=99, height=99, width=805)

        btn_cambiar_nombre = tk.Button(Frame, text=textos["cambiar_nombre"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1,
                                       command=cambiar_nombre)
        btn_cambiar_nombre.place(x=200, y=199, height=99, width=805)

        btn_cerrar_sesion = tk.Button(Frame, text=textos["cerrar_sesion"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1,
                                      command=Cerrar_sesion)
        btn_cerrar_sesion.place(x=200, y=299, height=99, width=805)

        btn_borrar_cuenta = tk.Button(Frame, text=textos["borrar_cuenta"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1)
        btn_borrar_cuenta.place(x=200, y=399, height=99, width=805)

        btn_datos_de_cuenta = tk.Button(Frame, text=textos["datos_de_cuenta"], bg=bg_actual, fg="#007BFF", font=("Arial", 20), bd=1)
        btn_datos_de_cuenta.place(x=200, y=399, height=99, width=805)
    else:
        messagebox.showwarning(textos["atencion"],textos["sin_cuenta"])
        actualizar_interfaz()



def Cambiar_contraseña():
    actualizar_interfaz()

    entrada_contraseña_actual = tk.Entry(
        Frame,
        bd=1,
        font=("Arial", 14),
        relief="flat",
        bg="#007BFF",
        fg=bg_actual,
        show="*"
    )
    entrada_contraseña_actual.place(x=270, y=110, width=410, height=30)

    entrada_contraseña_nueva = tk.Entry(
        Frame,
        bd=1,
        font=("Arial", 14),
        relief="flat",
        bg="#007BFF",
        fg=bg_actual,
        show="*"
    )
    entrada_contraseña_nueva.place(x=270, y=210, width=410, height=30)

    entrada_confirmar_contraseña = tk.Entry(
        Frame,
        bd=1,
        font=("Arial", 14),
        relief="flat",
        bg="#007BFF",
        fg=bg_actual,
        show="*"
    )
    entrada_confirmar_contraseña.place(x=270, y=310, width=410, height=30)

    label_contraseña_actual = tk.Label(
        Frame,
        text="Ingresar contraseña actual",
        font=("Arial", 12),
        bg=bg_actual,
        fg="#007BFF"
    )
    label_contraseña_actual.place(x=270, y=160)

    label_contraseña_nueva = tk.Label(
        Frame,
        text="Ingresar contraseña nueva",
        font=("Arial", 12),
        bg=bg_actual,
        fg="#007BFF"
    )
    label_contraseña_nueva.place(x=270, y=260)

    label_confirmar_contraseña = tk.Label(
        Frame,
        text="Confirmar contraseña nueva",
        font=("Arial", 12),
        bg=bg_actual,
        fg="#007BFF"
    )
    label_confirmar_contraseña.place(x=270, y=360)

    try:
        query = "SELECT * FROM usuarios WHERE Contraseña = %s"
        cursor.execute(query, (entrada_contraseña_actual.get(),))
        resultado = cursor.fetchone()

        if resultado:
            if entrada_contraseña_nueva.get() == entrada_confirmar_contraseña.get():
                update_query = "UPDATE usuarios SET Contraseña = %s WHERE Contraseña = %s"
                cursor.execute(update_query, (entrada_contraseña_nueva.get(), entrada_contraseña_actual.get()))
                conexion.commit()
                messagebox.showinfo("Listo", "Cambios realizados con éxito")
            else:
                messagebox.showerror("Error", "Las contraseñas nuevas no coinciden")
        else:
            messagebox.showerror("Error", "La contraseña actual no es correcta")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"No se ha podido actualizar la contraseña: {e}")

    Limpiar_Frame()
    Mostrar_barra_lateral()
def Cambiar_contraseña():
    actualizar_interfaz()

    label_contraseña_actual = tk.Label(
        Frame, 
        text="Ingresar contraseña actual", 
        font=("Arial", 12), 
        bg=bg_actual, 
        fg="#007BFF"
    )
    label_contraseña_actual.place(x=270, y=160)
    entrada_contraseña_actual = tk.Entry(
        Frame, 
        bd=1, 
        font=("Arial", 14), 
        relief="flat", 
        bg="#007BFF", 
        fg=bg_actual
    )
    entrada_contraseña_actual.place(x=270, y=110, width=410, height=30)

    label_contraseña_nueva = tk.Label(
        Frame, 
        text="Ingresar contraseña nueva", 
        font=("Arial", 12), 
        bg=bg_actual, 
        fg="#007BFF"
    )
    label_contraseña_nueva.place(x=270, y=260)
    entrada_contraseña_nueva = tk.Entry(
        Frame, 
        bd=1, 
        font=("Arial", 14), 
        relief="flat", 
        bg="#007BFF", 
        fg=bg_actual
    )
    entrada_contraseña_nueva.place(x=270, y=210, width=410, height=30)

    label_confirmar_contraseña = tk.Label(
        Frame, 
        text="Confirmar contraseña nueva", 
        font=("Arial", 12), 
        bg=bg_actual, 
        fg="#007BFF"
    )
    label_confirmar_contraseña.place(x=270, y=360)
    entrada_confirmar_contraseña = tk.Entry(
        Frame, 
        bd=1, 
        font=("Arial", 14), 
        relief="flat", 
        bg="#007BFF", 
        fg=bg_actual, 
        show="*"
    )
    entrada_confirmar_contraseña.place(x=270, y=310, width=410, height=30)

    def Cambio():
        try:
            query = "SELECT * FROM usuarios WHERE Contraseña = %s"
            cursor.execute(query, (entrada_contraseña_actual.get(),))
            resultado = cursor.fetchone()
            if resultado:
                if entrada_contraseña_nueva.get() == entrada_confirmar_contraseña.get():
                    update_query = "UPDATE usuarios SET Contraseña = %s WHERE Contraseña = %s"
                    cursor.execute(update_query, (entrada_contraseña_nueva.get(), entrada_contraseña_actual.get()))
                    conexion.commit()
                    messagebox.showinfo("Listo", "Cambios realizados con éxito")
                else:
                    messagebox.showerror("Error", "Las contraseñas nuevas no coinciden")
            else:
                messagebox.showerror("Error", "La contraseña actual no es correcta")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se ha podido actualizar la contraseña: {e}")

    boton_cambiar_contraseña = tk.Button(Frame, text="Cambiar contraseña",bg="#007BFF",fg=bg_actual,font=("Arial", 14), relief="flat", command=Cambio)
    boton_cambiar_contraseña.place(x=270, y=410)

def cambiar_nombre(): 
    actualizar_interfaz()
    label_usuario_actual = tk.Label(
        Frame, 
        text="Ingresar nombre de usuario actual", 
        font=("Arial", 12), 
        bg=bg_actual, 
        fg="#007BFF"
    )
    label_usuario_actual.place(x=270, y=160)

    entrada_usuario_actual = tk.Entry(
        Frame, 
        bd=1, 
        font=("Arial", 14), 
        relief="flat", 
        bg="#007BFF", 
        fg=bg_actual
    )
    entrada_usuario_actual.place(x=270, y=110, width=410, height=30)

    label_usuario_nuevo = tk.Label(
        Frame, 
        text="Ingresar nombre de usuario nuevo", 
        font=("Arial", 12), 
        bg=bg_actual, 
        fg="#007BFF"
    )
    label_usuario_nuevo.place(x=270, y=260)
    entrada_usuario_nuevo = tk.Entry(
        Frame, 
        bd=1, 
        font=("Arial", 14), 
        relief="flat", 
        bg="#007BFF", 
        fg=bg_actual
    )
    entrada_usuario_nuevo.place(x=270, y=210, width=410, height=30)

    label_confirmar_usuario = tk.Label(
        Frame, 
        text="Confirmar nombre de usuario", 
        font=("Arial", 12), 
        bg=bg_actual, 
        fg="#007BFF"
    )
    label_confirmar_usuario.place(x=270, y=360)
    entrada_confirmar_usuario = tk.Entry(
        Frame, 
        bd=1, 
        font=("Arial", 14), 
        relief="flat", 
        bg="#007BFF", 
        fg=bg_actual, 
        show="*"
    )
    entrada_confirmar_usuario.place(x=270, y=310, width=410, height=30)
    def Cambio_usuario():
        try:
            query = "SELECT * FROM usuarios WHERE Nombre = %s"
            cursor.execute(query, (entrada_usuario_actual.get(),))
            resultado = cursor.fetchone()
            if resultado:
                if entrada_usuario_nuevo.get() == entrada_confirmar_usuario.get():
                    update_query = "UPDATE usuarios SET Nombre = %s WHERE Nombre = %s"
                    cursor.execute(update_query, (entrada_usuario_nuevo.get(), entrada_usuario_actual.get()))
                    conexion.commit()
                    messagebox.showinfo("Listo", "Cambios realizados con éxito")
                else:
                    messagebox.showerror("Error", "El nombre de usuario no coincide")
            else:
                messagebox.showerror("Error", "Nombre de usuario incorrecto")
        except pymysql.Error as e:
            messagebox.showerror("Error", f"No se ha podido actualizar el nombre de usuario: {e}")

    boton_cambiar_usuario = tk.Button(Frame, text="Cambiar nombre de usuario", bg="#007BFF",fg=bg_actual,font=("Arial", 14), relief="flat", command=Cambio_usuario)
    boton_cambiar_usuario.place(x=270, y=410)

def Ver_acerca_de():
    actualizar_interfaz()

    Frame_titulo = tk.Frame(Frame, bg=bg_gris, bd=5)
    Frame_titulo.place(x=200, y=0, height=99, width=800)

    lbl_titulo = tk.Label(
        Frame_titulo,
        text="Acerca de",
        bg=bg_gris,
        fg="#007BFF",
        font=("Arial", 36, "bold")
    )
    lbl_titulo.place(x=10, y=20)

    Frame_creditos = tk.Frame(Frame, bg=bg_actual)
    Frame_creditos.place(x=200, y=100, width=800, height=400)

    creditos = (
        "- Khaleb Haziel Luis Reyes - Desarrollador\n\n"
        "- Sergio Alonso García Gonzáles - Desarrollador\n\n"
        "- Sara Guadalupe González Pérez - Desarrollador\n\n"
        "- Fabiola Carmona Trejo - Diseño/Documentación\n\n"
        "- César Eduardo Muñiz Aranda - Diseño/Documentación"
    )

    lbl_creditos = tk.Label(
        Frame_creditos,
        text=creditos,
        bg=bg_actual,
        fg="#007BFF",
        font=("Arial", 16),
        justify="left",
        anchor="nw"
    )
    lbl_creditos.pack()

def marcar_tarea_entregada(tarea_id, id_clase):
    try:
        query = "UPDATE tareas_cursas SET Estado = 'entregada' WHERE ID = %s"
        cursor.execute(query, (tarea_id,))
        conexion.commit()
        messagebox.showinfo("Éxito", "Tarea marcada como entregada.")
        verTareas(id_clase)
    except pymysql.Error as e:
        messagebox.showerror("Error", f"No se pudo actualizar el estado de la tarea: {e}")

def calcular_progreso(id_clase):
    try:
        query_total = "SELECT COUNT(*) FROM tareas_cursas WHERE ID_Clase = %s"
        cursor.execute(query_total, (id_clase,))
        total = cursor.fetchone()[0]

        query_entregadas = "SELECT COUNT(*) FROM tareas_cursas WHERE ID_Clase = %s AND Estado = 'entregada'"
        cursor.execute(query_entregadas, (id_clase,))
        entregadas = cursor.fetchone()[0]

        if total == 0:
            progreso = 0
        else:
            progreso = (entregadas / total) * 100

        messagebox.showinfo("Progreso", f"El progreso actual es del {progreso:.2f}%")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"No se pudo calcular el progreso: {e}")

def Iniciar_app():
    global Frame, conexion, cursor, lbl_logo
    Frame = tk.Tk()
    Frame.title("AcadeMix")
    Frame.geometry("1000x600+200+50")
    Frame.config(bg=bg_actual)
    Frame.resizable(False, False)

    logo_path = resource_path("images/Logo.png")
    logo = ImageTk.PhotoImage(file=logo_path)
    Frame.iconphoto(False, logo)
    Frame.resizable(False, False)

    imagen = Image.open(logo_path)
    imagen = imagen.resize(( 90, 90), Image.LANCZOS)
    
    imagen_logo = ImageTk.PhotoImage(imagen) 

    lbl_logo = tk.Label(Frame, image=imagen_logo, bg=bg_actual)
    lbl_logo.pack(anchor="se",side=tk.BOTTOM)

    try:
        conexion = pymysql.connect(
            user="root",
            database="Academix_DB",
            host="localhost",
            password=""
        )
        cursor = conexion.cursor()
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error al conectar a la base de datos: {e}")
        return

    verificar_sesion_activa()

    Frame.mainloop()

textos = cargar_lenguaje("es.json")

Iniciar_app()