import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Función para guardar los registros en un archivo de texto
def guardar_registros():
    with open('registros.txt', 'w') as f:
        for registro in registros:
            f.write(','.join(registro) + '\n')

# Función para cargar los registros desde un archivo de texto
def cargar_registros():
    try:
        with open('registros.txt', 'r') as f:
            return [line.strip().split(',') for line in f.readlines()]
    except FileNotFoundError:
        return []

# Lista de personas y vehículos ingresados
registros = cargar_registros()
registros_salida = []

# Función para registrar ingreso de una persona
def registrar_ingreso():
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    documento = entry_documento.get()
    fecha_nacimiento = entry_fecha_nacimiento.get()
    tipo_ingresante = tipo_ingresante_var.get()  # Obtener el tipo de ingresante seleccionado

    if tipo_ingresante == "Propietario":
        numero_telefono = entry_telefono.get()
        numero_lote = entry_lote.get()
    else:
        numero_telefono = ""
        numero_lote = ""

    if nombre and apellido and documento and fecha_nacimiento and tipo_ingresante:
        ahora = datetime.now()
        hora_ingreso = ahora.strftime("%H:%M:%S")
        registros.append([nombre, apellido, documento, fecha_nacimiento, hora_ingreso, tipo_ingresante, numero_telefono, numero_lote, "Dentro"])
        guardar_registros()
        actualizar_lista()  # Llamar a actualizar_lista después de agregar el nuevo registro
        messagebox.showinfo("Ingreso registrado", "Ingreso registrado correctamente")
    else:
        messagebox.showerror("Error", "Por favor completa todos los campos")

# Función para actualizar la lista de personas y vehículos ingresados
def actualizar_lista():
    lista_registros.delete(0, tk.END)
    for registro in registros:
        texto = f"Nombre: {registro[0]} - Apellido: {registro[1]} - Documento: {registro[2]}\nFecha de nacimiento: {registro[3]}\nHora ingreso: {registro[4]}\nTipo de ingresante: {registro[5]}\nNúmero de teléfono: {registro[6]}\nNúmero de lote: {registro[7]}\nEstado: {registro[8]}"
        lista_registros.insert(tk.END, texto)

# Función para buscar y dar salida a una persona
def dar_salida():
    texto_busqueda = entry_busqueda.get()
    for i, registro in enumerate(registros.copy()):
        if texto_busqueda in registro:
            ahora = datetime.now()
            hora_salida = ahora.strftime("%H:%M:%S")
            registros[i].append(hora_salida)
            registros[i].append("Fuera")
            registros_salida.append(registro)
            registros.remove(registro)
            actualizar_lista()
            actualizar_lista_salida()
            guardar_registros()
            messagebox.showinfo("Salida registrada", f"Salida registrada correctamente para {registro[0]} {registro[1]}.\nHora de salida: {hora_salida}")
            return
    messagebox.showerror("Error", "No se encontró a la persona")

# Función para actualizar la lista de personas que se retiraron
def actualizar_lista_salida():
    lista_registros_salida.delete(0, tk.END)
    for registro in registros_salida:
        texto = f"Nombre: {registro[0]} - Apellido: {registro[1]} - Documento: {registro[2]}\nFecha de nacimiento: {registro[3]}\nHora salida: {registro[6]}\nTipo de ingresante: {registro[5]}\nNúmero de teléfono: {registro[7]}\nNúmero de lote: {registro[8]}"
        lista_registros_salida.insert(tk.END, texto)

# Crear ventana
ventana = tk.Tk()
ventana.title("Control de Acceso")
ventana.geometry("800x600")

# Cambiar el color de fondo de la ventana
ventana.configure(bg="#708090")

# Contenedor principal
frame_principal = ttk.Frame(ventana)
frame_principal.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

# Contenido para la lista general
# Etiquetas y campos de entrada
ttk.Label(frame_principal, text="Datos del ingresante").grid(row=0, column=0, columnspan=2, padx=5, pady=5)
ttk.Label(frame_principal, text="Nombre:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
ttk.Label(frame_principal, text="Apellido:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
ttk.Label(frame_principal, text="Documento:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
ttk.Label(frame_principal, text="Fecha de nacimiento:").grid(row=4, column=0, padx=5, pady=5, sticky="w")

entry_nombre = ttk.Entry(frame_principal)
entry_apellido = ttk.Entry(frame_principal)
entry_documento = ttk.Entry(frame_principal)
entry_fecha_nacimiento = ttk.Entry(frame_principal)

entry_nombre.grid(row=1, column=1, padx=5, pady=5, sticky="w")
entry_apellido.grid(row=2, column=1, padx=5, pady=5, sticky="w")
entry_documento.grid(row=3, column=1, padx=5, pady=5, sticky="w")
entry_fecha_nacimiento.grid(row=4, column=1, padx=5, pady=5, sticky="w")

# Etiqueta y campo para el tipo de ingresante
ttk.Label(frame_principal, text="Tipo de ingresante:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
tipo_ingresante_var = tk.StringVar(value="Propietario")
tipo_ingresante_combobox = ttk.Combobox(frame_principal, textvariable=tipo_ingresante_var, values=["Propietario", "Visitante"])
tipo_ingresante_combobox.grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Campos adicionales para propietarios
ttk.Label(frame_principal, text="Número de teléfono:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
ttk.Label(frame_principal, text="Número de lote:").grid(row=7, column=0, padx=5, pady=5, sticky="w")

entry_telefono = ttk.Entry(frame_principal)
entry_lote = ttk.Entry(frame_principal)

# Función para ocultar los campos de teléfono y lote cuando el ingresante es visitante
def ocultar_campos():
    if tipo_ingresante_var.get() == "Propietario":
        entry_telefono.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        entry_lote.grid(row=7, column=1, padx=5, pady=5, sticky="w")
    else:
        entry_telefono.grid_remove()
        entry_lote.grid_remove()

ocultar_campos()  # Llamar a la función para asegurarse de que los campos estén ocultos o visibles al iniciar la ventana

# Botón para registrar ingreso
ttk.Button(frame_principal, text="Registrar Ingreso", command=registrar_ingreso).grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Lista de personas y vehículos ingresados
lista_registros = tk.Listbox(frame_principal, height=10, width=60)
lista_registros.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Barra de desplazamiento para la lista de personas y vehículos ingresados
scrollbar_registros = ttk.Scrollbar(frame_principal, orient=tk.VERTICAL, command=lista_registros.yview)
scrollbar_registros.grid(row=9, column=2, sticky="ns")
lista_registros.config(yscrollcommand=scrollbar_registros.set)

# Contenedor para la búsqueda, dar salida y lista de personas que se retiraron
frame_derecho = ttk.Frame(ventana)
frame_derecho.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

# Etiqueta y campo de búsqueda para dar salida
ttk.Label(frame_derecho, text="Buscar ").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_busqueda = ttk.Entry(frame_derecho)
entry_busqueda.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
ttk.Button(frame_derecho, text="Dar Salida", command=dar_salida).grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Lista de personas que se retiraron
lista_registros_salida = tk.Listbox(frame_derecho, height=10, width=60)
lista_registros_salida.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

# Barra de desplazamiento para la lista de personas que se retiraron
scrollbar_registros_salida = ttk.Scrollbar(frame_derecho, orient=tk.VERTICAL, command=lista_registros_salida.yview)
scrollbar_registros_salida.grid(row=2, column=2, sticky="ns")
lista_registros_salida.config(yscrollcommand=scrollbar_registros_salida.set)

# Etiqueta de estado
etiqueta_estado = ttk.Label(frame_principal, text="Estado:", background="gray")
etiqueta_estado.grid(row=10, column=0, padx=5, pady=5, sticky="w")

# Ejecutar ventana
ventana.mainloop()
