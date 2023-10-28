import tkinter as tk
from tkinter import ttk
import controller as q
from tkinter import ttk, messagebox
import data
import sys
import os

datos = data.partido

base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.abspath(".")
db_path = os.path.join(base_path, "partidos_politicos.db")


def validate_input(P):
    if P == "":
        return True
    if len(P) == 1 and P == "0":
        return False
    if P.isdigit() and len(P) <= 2:
        return True
    return False


def limpiar_entradas(entry_dict):
    for entry in entry_dict.values():
        entry.delete(0, "end")


def centro_democratico(frame, mesa):
    entry_dict = {}
    frame_centro_democratico = ttk.Frame(frame)
    frame_centro_democratico.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_centro_democratico = datos['Centro Democratico']

    for candidato in candidatos_centro_democratico:
        label_candidato = tk.Label(frame_centro_democratico, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_centro_democratico.register(
            validate_input)
        entry = tk.Entry(frame_centro_democratico, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()
        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            candidatos.append(candidato)
            if not entry.get():
                datos.append(0)
            else:
                datos.append(int(entry.get()))

        if not datos:
            messagebox.showerror(
                "Error", "Ingresa al menos un voto antes de guardar.")
            return

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "centro_democratico", candidatos, mesa)
        existe = registro.mesa_exists()
        registro.create_table()
        if existe:
            registro.update_data(datos)
        else:
            registro.insert_data(datos)

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)
        registro.close_connection

    boton_recolectar = tk.Button(
        frame_centro_democratico, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def salvacion_nacional(frame, mesa):
    entry_dict = {}
    frame_salvacion_nacional = ttk.Frame(frame)
    frame_salvacion_nacional.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_salvacion_nacional = datos['Movimiento Salvacion Nacional']

    for candidato in candidatos_salvacion_nacional:
        label_candidato = tk.Label(frame_salvacion_nacional, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_salvacion_nacional.register(
            validate_input)
        entry = tk.Entry(frame_salvacion_nacional, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()
        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "salvacion_nacional", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_salvacion_nacional, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def conservador(frame, mesa):
    entry_dict = {}
    frame_conservador = ttk.Frame(frame)
    frame_conservador.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_conservador = datos['Conservador']

    for candidato in candidatos_conservador:
        label_candidato = tk.Label(frame_conservador, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_conservador.register(validate_input)
        entry = tk.Entry(frame_conservador, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "conservador", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_conservador, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def partido_u(frame, mesa):
    entry_dict = {}
    frame_la_u = ttk.Frame(frame)
    frame_la_u.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_la_u = datos['La U']

    for candidato in candidatos_la_u:
        label_candidato = tk.Label(frame_la_u, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_la_u.register(validate_input)
        entry = tk.Entry(frame_la_u, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "partido_la_u", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_la_u, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def liberal(frame, mesa):
    entry_dict = {}
    frame_liberal = ttk.Frame(frame)
    frame_liberal.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_liberal = datos['Liberal']

    for candidato in candidatos_liberal:
        label_candidato = tk.Label(frame_liberal, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_liberal.register(validate_input)
        entry = tk.Entry(frame_liberal, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "Liberal", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_liberal, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def creemos(frame, mesa):
    entry_dict = {}
    frame_creemos = ttk.Frame(frame)
    frame_creemos.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_creemos = datos['Creemos']

    for candidato in candidatos_creemos:
        label_candidato = tk.Label(frame_creemos, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_creemos.register(validate_input)
        entry = tk.Entry(frame_creemos, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "Creemos", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_creemos, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def nuevo_liberalismo(frame, mesa):
    entry_dict = {}
    frame_nuevo_liberalismo = ttk.Frame(frame)
    frame_nuevo_liberalismo.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_nuevo_liberalismo = datos['Nuevo Liberalismo']

    for candidato in candidatos_nuevo_liberalismo:
        label_candidato = tk.Label(frame_nuevo_liberalismo, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_nuevo_liberalismo.register(
            validate_input)
        entry = tk.Entry(frame_nuevo_liberalismo, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "nuevo_liberalismo", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_nuevo_liberalismo, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def cambio_radical(frame, mesa):
    entry_dict = {}
    frame_cambio_radical = ttk.Frame(frame)
    frame_cambio_radical.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_cambio_radical = datos['Cambio Radical']

    for candidato in candidatos_cambio_radical:
        label_candidato = tk.Label(frame_cambio_radical, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_cambio_radical.register(validate_input)
        entry = tk.Entry(frame_cambio_radical, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "cambio_radical", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_cambio_radical, text="Recolectar Datos", command=recolectar_datos, padx=5, pady=5)
    boton_recolectar.pack()


def alianza_verde(frame, mesa):
    entry_dict = {}
    frame_alianza_verde = ttk.Frame(frame)
    frame_alianza_verde.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_alianza_verde = datos['Alianza Verde']

    for candidato in candidatos_alianza_verde:
        label_candidato = tk.Label(frame_alianza_verde, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_alianza_verde.register(validate_input)
        entry = tk.Entry(frame_alianza_verde, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        # print(datos)

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "alianza_verde", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_alianza_verde, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def voto_en_blanco(frame, mesa):
    entry_dict = {}
    frame_voto_blanco = ttk.Frame(frame)
    frame_voto_blanco.pack(padx=3, pady=3, fill="both", expand=True)
    candidatos_votos_blanco = ["Votos en blanco", "Votos nulos"]

    for candidato in candidatos_votos_blanco:
        label_candidato = tk.Label(frame_voto_blanco, text=candidato)
        label_candidato.pack()
        validate_input_command = frame_voto_blanco.register(validate_input)
        entry = tk.Entry(frame_voto_blanco, validate="key",
                         validatecommand=(validate_input_command, "%P"))
        entry.pack()

        entry_dict[candidato] = entry

    def recolectar_datos():
        datos = []
        candidatos = []

        for candidato, entry in entry_dict.items():
            if not entry.get():
                candidatos.append(candidato)
                datos.append(0)
            else:
                candidatos.append(candidato)
                datos.append(int(entry.get()))
        print(datos, "RECOLECTAR DATOS VOTOS EN BLANCO")

        registro = q.PartidoPoliticoDB(
            "partidos_politicos.db", "voto_blanco", candidatos, mesa)
        existe = registro.mesa_exists()
        # print(existe)
        registro.create_table()
        if existe:
            # print(0, existe)
            # print("La mesa ya existe")
            registro.update_data(datos)
        else:
            # print(1, existe)
            registro.insert_data(datos)
        registro.close_connection

        messagebox.showinfo("Éxito", "Los datos se han guardado con éxito.")
        limpiar_entradas(entry_dict)

    boton_recolectar = tk.Button(
        frame_voto_blanco, text="Recolectar Datos", command=recolectar_datos)
    boton_recolectar.pack()


def formulario(form):
    forms = {
        'centro democratico': centro_democratico(),
        'salvacion nacional': salvacion_nacional(),
        'conservador': conservador(),
        'u': partido_u(),
        'liberal': liberal(),
        'creemos': creemos(),
        'nuevo liberalismo': nuevo_liberalismo(),
        'cambio radical': cambio_radical(),
        'alianza verde': alianza_verde(),
        'votos en blanco': voto_en_blanco()
    }
    xform = forms[form]
