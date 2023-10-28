import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import formularios as f
import controller as q
import data
import sqlite3
import os


def eliminar_base_de_datos():
    confirmacion = messagebox.askyesno(
        "Advertencia", "¿Estas seguro de eliminar todas las mesas?")
    if confirmacion:
        try:

            db_path = "partidos_politicos.db"
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table';")
            tablas = cursor.fetchall()

            for tabla in tablas:
                tabla_nombre = tabla[0]
                cursor.execute(f"DELETE FROM {tabla_nombre};")
            conn.commit()
            conn.close()

            # print("Se han eliminado todos los registros de todas las tablas en la base de datos.")
            db = q.MesasDb('partidos_politicos.db')
            db.create_mesa()
            nro_mesas = db.conteo_mesas()
            # print(nro_mesas)
            mostrar_datos_treeview(nro_mesas, db)

        except sqlite3.Error as e:
            print(f"Error al borrar registros en todas las tablas: {e}")


def validate_input(P):
    if P == "":
        return True
    if len(P) == 1 and P == "0":
        return False
    if P.isdigit() and len(P) <= 2:
        return True
    return False


def borrar_texto():
    ErroresLabel.pack_forget()
    Errores_Var.set("")


def actualizar_seleccion_partido(*args):
    partido_seleccionado = partido_var.get()
    numeroMesaSeleccionada = seleccion_mesa_label.cget(
        "text")
    seleccion_partido_var.set(f"Partido {partido_seleccionado}")
    # print(partido_seleccionado)
    if (numeroMesaSeleccionada == ""):
        seleccion_partido_var.set("")
        ErroresLabel.pack()
        Errores_Var.set("Seleccione un mesa primero")
        root.after(1000, borrar_texto)
    else:
        # print("Mesa en envio de datos:", numeroMesaSeleccionada)
        limpiar_frame(middle_frame)
        if partido_seleccionado == "CambioRadical":
            f.cambio_radical(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "CentroDemocratico":
            f.centro_democratico(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "Conservador":
            f.conservador(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "Creemos":
            f.creemos(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "LaU":
            f.partido_u(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "Liberal":
            f.liberal(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "NuevoLiberalismo":
            f.nuevo_liberalismo(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "SalvacionNacional":
            f.salvacion_nacional(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "Verde":
            f.alianza_verde(middle_frame, numeroMesaSeleccionada)
        elif partido_seleccionado == "votosEnBlanco":
            f.voto_en_blanco(middle_frame, numeroMesaSeleccionada)
        else:
            ErroresLabel.pack()
            Errores_Var.set("Selecciona otro")
            root.after(1000, borrar_texto)
        partido_seleccionado = partido_var.get()
        seleccion_partido_var.set(f"Partido {partido_seleccionado}")
        frame_botones.pack(side="top", padx=10, pady=10)


def MostrarFramePrincipal():
    FramePrincipal.pack(fill='both', expand=True)
    FrameTotalizarVotos.pack_forget()
    for widget in FrameTotalizarVotos.winfo_children():
        widget.destroy()


def MostrarFrameTotalizarVotos():
    for widget in FrameTotalizarVotos.winfo_children():
        widget.destroy()
    FrameTotalizarVotos.pack(fill='both', expand=True)
    FramePrincipal.pack_forget()
    frame_derecho = tk.Frame(FrameTotalizarVotos)
    frame_izquierdo = tk.Frame(FrameTotalizarVotos)
    frame_derecho.pack(side='right', fill='y')
    frame_izquierdo.pack(side='left', fill='y')
    frame_calcular = tk.Frame(frame_derecho)
    frame_calcular.pack(side='bottom', fill='y', pady=100)
    datos = data.partido

    def calcular():
        for widget in frame_calcular.winfo_children():
            widget.destroy()
        for widget in frame_izquierdo.winfo_children():
            widget.destroy()
        numeroCurules = entry.get()
        if (numeroCurules == ""):
            print("Digite un numero", numeroCurules)
        else:

            umbralLabel = crear_recuadro(
                frame_calcular, "Umbral", round((votosValidos/int(numeroCurules))/2))
            umbral = round((votosValidos/int(numeroCurules))/2)
            partidosAptos = []
            for partido in votosPorPartido:
                for nombre_partido, lista_votos in partido.items():
                    primer_numero = lista_votos[0]
                    # print(f"El primer número de {nombre_partido} es mayor que {umbral}")
                    if primer_numero > int(umbral):
                        partidosAptos.append({nombre_partido: lista_votos})
                        # print(f"El primer número de {nombre_partido} es mayor que {umbral}")
            frame_tabla = tk.Frame(frame_izquierdo)
            frame_tabla.pack()
            todos_los_numeros = []
            for partido in partidosAptos:
                todos_los_numeros.extend(list(partido.values())[0])

            numeros_mayores = sorted(todos_los_numeros, reverse=True)[:11]
            cuocienteLabel = crear_recuadro(
                frame_calcular, "Cuociente", numeros_mayores[-1])
            nuevos_partidosAptos = []
            for partido in partidosAptos:
                nombre_partido, lista_votos = list(partido.items())[0]
                nuevos_valores = []
                for valor in lista_votos:
                    if valor in numeros_mayores:
                        nuevos_valores.append(f'***{valor}***')
                    else:
                        nuevos_valores.append(valor)
                nuevos_partido = {nombre_partido: nuevos_valores}
                nuevos_partidosAptos.append(nuevos_partido)

            if nuevos_partidosAptos:
                tree = ttk.Treeview(
                    frame_tabla, columns=nuevos_partidosAptos)
                nombres_partidos = [list(partido.keys())[0]
                                    for partido in nuevos_partidosAptos]
                num_divisiones = max(
                    len(list(partido.values())[0]) for partido in nuevos_partidosAptos)

                columnas = ['#'] + nombres_partidos
                tree['columns'] = columnas

                tree.heading('#', text='#')
                tree.column('#', width=50)
                tree.column('#0', width=5)

                for partido in nombres_partidos:
                    tree.heading(partido, text=partido)
                    tree.column(partido, width=100)

                for i in range(1, num_divisiones + 1):
                    valores = [i]
                    for partido in nuevos_partidosAptos:
                        lista_votos = list(partido.values())[0]
                        if i <= len(lista_votos):
                            valores.append(lista_votos[i-1])
                        else:
                            valores.append('')
                    tree.insert('', 'end', values=valores)
                tree.pack()
            else:
                messagebox.showinfo("Error", "No hay datos para mostrar")

    candidatosCentroDemocratico = datos['Centro Democratico']
    candidatosSalvacionNacional = datos['Movimiento Salvacion Nacional']
    candidatosConservador = datos['Conservador']
    candidatosLaU = datos['La U']
    candidatosLiberal = datos['Liberal']
    candidatosCreemos = datos['Creemos']
    candidatosNuevoLiberalismo = datos['Nuevo Liberalismo']
    candidatosCambioRadical = datos['Cambio Radical']
    candidatosAlianzaVerde = datos['Alianza Verde']
    candidatosVotosBlanco = ["Votos en blanco"]

    votosCentroDemocratico = q.PartidoPoliticoDB(
        "partidos_politicos.db", "centro_democratico", candidatosCentroDemocratico, 0)
    totalVotosCentroDemocratico = votosCentroDemocratico.recolectarDatos()

    votosSalvacionNacional = q.PartidoPoliticoDB(
        "partidos_politicos.db", "salvacion_nacional", candidatosSalvacionNacional, 0)
    totalVotosSalvacionNacional = votosSalvacionNacional.recolectarDatos()

    votosConservador = q.PartidoPoliticoDB(
        "partidos_politicos.db", "conservador", candidatosConservador, 0)
    totalVotosConservador = votosConservador.recolectarDatos()

    votosLaU = q.PartidoPoliticoDB(
        "partidos_politicos.db", "partido_la_u", candidatosLaU, 0)
    totalVotosLaU = votosLaU.recolectarDatos()

    votosLiberal = q.PartidoPoliticoDB(
        "partidos_politicos.db", "Liberal", candidatosLiberal, 0)
    totalVotosLiberal = votosLiberal.recolectarDatos()

    votosCreemos = q.PartidoPoliticoDB(
        "partidos_politicos.db", "Creemos", candidatosCreemos, 0)
    totalVotosCreemos = votosCreemos.recolectarDatos()

    votosNuevoLiberalismo = q.PartidoPoliticoDB(
        "partidos_politicos.db", "nuevo_liberalismo", candidatosNuevoLiberalismo, 0)
    totalVotosNuevoLiberalismo = votosNuevoLiberalismo.recolectarDatos()

    votosCambioRadical = q.PartidoPoliticoDB(
        "partidos_politicos.db", "cambio_radical", candidatosCambioRadical, 0)
    totalVotosCambioRadical = votosCambioRadical.recolectarDatos()

    votosVerde = q.PartidoPoliticoDB(
        "partidos_politicos.db", "alianza_verde", candidatosAlianzaVerde, 0)
    totalVotosVerde = votosVerde.recolectarDatos()

    VotosEnBlanco = q.PartidoPoliticoDB(
        "partidos_politicos.db", "voto_blanco", candidatosVotosBlanco, 0)
    totalVotosEnBlanco = VotosEnBlanco.recolectarDatos()

    votosValidos = totalVotosCambioRadical + totalVotosCentroDemocratico + totalVotosConservador + totalVotosCreemos + totalVotosLaU + \
        totalVotosLiberal + totalVotosNuevoLiberalismo + \
        totalVotosSalvacionNacional + totalVotosEnBlanco + totalVotosVerde

    # print(votosValidos)

    def crear_recuadro(parent, texto, valor):
        frame = tk.Frame(parent)
        frame.pack(pady=5)
        font_negrita = ("Arial", 10, "bold")

        label = tk.Label(frame, text=f"{texto}:", font=font_negrita, width=20)
        label.pack(side="left")

        valor_label = tk.Label(frame, text=valor, font=font_negrita, width=20)
        valor_label.pack(side="right")

    votosSalvacionLabel = crear_recuadro(
        frame_derecho, "Salvacion nacional", totalVotosSalvacionNacional)
    votosVerdeLabel = crear_recuadro(
        frame_derecho, "Partido verde", totalVotosVerde)
    votosCambioRadicalLabel = crear_recuadro(
        frame_derecho, "Cambio radical", totalVotosCambioRadical)
    votosNuevoLiberalismoLabel = crear_recuadro(
        frame_derecho, "Nuevo liberalismo", totalVotosNuevoLiberalismo)
    votosBlancosLabel = crear_recuadro(
        frame_derecho, "Votos en blanco", totalVotosEnBlanco)
    votosLaULabel = crear_recuadro(
        frame_derecho, "Partido de la u", totalVotosLaU)
    votosCreemosLabel = crear_recuadro(
        frame_derecho, "Creemos", totalVotosCreemos)
    votosLiberalLabel = crear_recuadro(
        frame_derecho, "Liberal", totalVotosLiberal)
    votosConservadorLabel = crear_recuadro(
        frame_derecho, "Conservador", totalVotosConservador)
    votosCentroDemocraticoLabel = crear_recuadro(
        frame_derecho, "Centro democratico", totalVotosCentroDemocratico)
    separator = ttk.Separator(frame_derecho, orient="horizontal")
    separator.pack(fill="x", padx=10, pady=10)
    VotosTotalesLabel = crear_recuadro(
        frame_derecho, "Votos válidos", votosValidos)
    label_candidato = tk.Label(frame_derecho, text="Curules")
    label_candidato.pack()
    entry = tk.Entry(frame_derecho, validate="key",
                     validatecommand=(validate_input_command, "%P"))
    entry.pack()
    botonCalcular = tk.Button(
        frame_derecho, text="Calcular", command=calcular)
    botonCalcular.pack()
    votosPorPartido = [
        {'Movimiento Salvacion Nacional': totalVotosSalvacionNacional},
        {'Centro Democratico': totalVotosCentroDemocratico},
        {'Conservador': totalVotosConservador},
        {'La U': totalVotosLaU},
        {'Liberal': totalVotosLiberal},
        {'Creemos': totalVotosCreemos},
        {'Nuevo Liberalismo': totalVotosNuevoLiberalismo},
        {'Cambio Radical': totalVotosCambioRadical},
        {'Alianza Verde': totalVotosVerde},
    ]
    num_divisiones = 11

    for partido_dict in votosPorPartido:
        partido, total_votos = list(partido_dict.items())[0]
        divisiones = [round(total_votos / (i + 1), 2)
                      for i in range(num_divisiones)]
        partido_dict[partido] = divisiones


def limpiar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def BarraMenu(root):
    barraMenu = tk.Menu(root)
    root.config(menu=barraMenu, width=300, height=300)

    menuInicio = tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label='Inicio', menu=menuInicio)
    menuInicio.add_command(label='Pantalla inicial',
                           command=MostrarFramePrincipal)
    menuInicio.add_command(label='Totalizar votos válidos',
                           command=MostrarFrameTotalizarVotos)
    menuInicio.add_command(label='Cerrar ventana', command=root.destroy)

    barraConfig = tk.Menu(barraMenu, tearoff=0)
    barraMenu.add_cascade(label='configuracion db', menu=barraConfig)
    barraConfig.add_command(
        label='Eliminar todas las mesas', command=eliminar_base_de_datos)


def actualizar_mesa_label(numeroMesa):
    texto = f"Mesa {numeroMesa}"
    seleccion_mesa_label.config(text=texto)


def mostrar_datos_treeview(datos, db):
    tree.delete(*tree.get_children())
    if datos:
        for dato in datos:
            tree.insert("", "end", values=(dato,))
    tree.column('Mesas', width=200)
    tree.grid(row=3, column=0, sticky="nsew")

    def mostrar_seleccion(event):
        confirmacion = messagebox.askyesno(
            "Confirmar eliminación", f"¿Está seguro de cambiar de mesa?")
        if (confirmacion):
            limpiar_frame(middle_frame)
            seleccion_partido_var.set("")
            item_seleccionado = tree.focus()
            valores = tree.item(item_seleccionado, "values")
            if valores:
                numero = valores[0]
                # print(f"Seleccionaste el número: {numero}")
                actualizar_mesa_label(numero)

    def agregar_mesa():
        db.agregar_mesa()
        if datos:
            nueva_mesa = datos[-1] + 1
        else:
            nueva_mesa = 1
        datos.append(nueva_mesa)
        tree.insert("", "end", values=(nueva_mesa,))

    def borrar_registro():
        limpiar_frame(middle_frame)
        seleccion_partido_var.set("")
        seleccion_mesa_label.config(text="")
        elementos = tree.get_children()
        if elementos:
            ultima_mesa = datos[-1]
            confirmacion = messagebox.askyesno(
                "Confirmar eliminación", f"¿Está seguro de eliminar la mesa {ultima_mesa}")

            if confirmacion:
                ultimo_elemento = elementos[-1]
                db.eliminar_mesa()
                datos.pop()
                tree.delete(ultimo_elemento)
        else:
            print("No hay mesas para eliminar")

    boton_agregar = tk.Button(
        frame_mesas, text="Agregar", command=agregar_mesa)
    boton_agregar.grid(row=2, column=0, pady=(0, 10))
    boton_eliminar = tk.Button(
        frame_mesas, text="Eliminar Ultima Mesa", command=borrar_registro)
    boton_eliminar.grid(row=4, column=0, pady=(0, 10))
    tree.bind("<<TreeviewSelect>>", mostrar_seleccion)


root = tk.Tk()
root.title("Sistema de Repartición de Curules")
root.state('zoomed')

partido_var = tk.StringVar()
seleccion_mesa_var = tk.StringVar()
seleccion_partido_var = tk.StringVar()
Errores_Var = tk.StringVar()

FramePrincipal = tk.Frame(root)
FrameTotalizarVotos = tk.Frame(root)
MostrarFramePrincipal()
frame_mesas = ttk.Frame(FramePrincipal)
frame_mesas.pack(side="left", fill="y")
frame_mesas = ttk.Frame(FramePrincipal)
frame_mesas.pack(side="left", fill="y")

tree = ttk.Treeview(frame_mesas, columns=('Mesas',), show='headings')
tree.heading('Mesas', text='Mesas')
validate_input_command = root.register(validate_input)

partido_imagenes = {}

# Ruta al directorio de imágenes (mismo nivel que main.py)
ruta_imgs = os.path.join(os.path.dirname(__file__), "imgs")

# Verificar si la carpeta existe
if os.path.exists(ruta_imgs):
    for filename in os.listdir(ruta_imgs):
        if filename.endswith(".jpg"):  # Asegúrate de que sean archivos JPG
            nombre_partido = os.path.splitext(filename)[0]
            ruta_imagen = os.path.join(ruta_imgs, filename)
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((50, 50))  # Ajustar tamaño a 50x50
            imagen_tk = ImageTk.PhotoImage(imagen)
            partido_imagenes[nombre_partido] = imagen_tk
else:
    print(f"La carpeta de imágenes no se encuentra en {ruta_imgs}")

frame_botones = ttk.Frame(FramePrincipal)
frame_botones.pack(side="top", padx=10, pady=10)


db = q.MesasDb('partidos_politicos.db')
db.create_mesa()
nro_mesas = db.conteo_mesas()
mostrar_datos_treeview(nro_mesas, db)

frame_mesas.grid_rowconfigure(3, weight=1)


seleccion_mesa_var.trace("w", actualizar_mesa_label)

for partido, imagen in partido_imagenes.items():
    boton = ttk.Button(frame_botones, image=imagen,
                       command=lambda p=partido: partido_var.set(p))
    boton.pack(side="left", padx=5)

frame_span = ttk.Frame(FramePrincipal)
frame_span.pack(side="top", padx=10)

seleccion_mesa_label = tk.Label(
    frame_span, text="")
seleccion_mesa_label.config(font=("Helvetica", 16))
seleccion_mesa_label.pack(side="top")

ErroresLabel = tk.Label(
    frame_span, textvariable=Errores_Var)
ErroresLabel.config(font=("Helvetica", 16))
ErroresLabel.pack(side="bottom")

seleccion_partido_label = tk.Label(
    frame_span, textvariable=seleccion_partido_var)
seleccion_partido_label.config(font=("Helvetica", 16))
seleccion_partido_label.pack(side="top")

middle_frame = ttk.Frame(FramePrincipal, borderwidth=2, relief="solid")
middle_frame.pack(fill="both", expand=True)

partido_var.trace_add("write", actualizar_seleccion_partido)
BarraMenu(root)
root.mainloop()
