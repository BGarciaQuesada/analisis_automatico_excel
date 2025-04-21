import os
import pandas as pd
import tkinter as tk
from tkinter import ttk

def comprobar_datos(root):
    # Encontrar directorio de datos y qué se debe de encontrar dentro de este
    datos_dir = 'datos'
    # [!!!] Sustituir......
    archivos_requeridos = ['regimen_general.xls', 'todas_las_ensenanzas.xls', 'ensenanza_de_adultos.xls']
    archivos_presentes = os.listdir(datos_dir)

    resultado = []

    # Bucle de comprobación
    for archivo in archivos_requeridos:
        if archivo in archivos_presentes:
            # ¿Está? Saca el año de dicho archivo y muestra un tic
            try:
                df = pd.read_excel(os.path.join(datos_dir, archivo))
                curso = df.iloc[0, 0]  # Suponiendo que el curso está en la primera fila, primera columna (Revisar......)
                resultado.append((f"✅ {archivo}", f"Curso: {curso}"))
            except Exception as e:
                # Error si no se ha podido añadir a la cadena de texto por algún motivo
                resultado.append((f"❌ {archivo}", f"Error: {str(e)}"))
        else:
            # ¿No está? Devolver cruz
            resultado.append((f"❌ {archivo}", "Archivo no encontrado"))

    # Creación de root (ventana)
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados de Comprobación")

    # --- INTERFAZ GRÁFICA (WIP) ---
    tree = ttk.Treeview(ventana_resultados, columns=("Estado", "Detalle"), show="headings")
    tree.heading("Estado", text="Estado")
    tree.heading("Detalle", text="Detalle")
    tree.pack(expand=True, fill=tk.BOTH)

    for estado, detalle in resultado:
        tree.insert("", "end", values=(estado, detalle))
