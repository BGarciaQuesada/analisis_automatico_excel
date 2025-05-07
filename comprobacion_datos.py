import os
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk

# Encontrar directorio de datos y qué se debe de encontrar dentro de este
def comprobar_datos(root):
    datos_dir = 'datos'

    # Comprobación de la existencia del directorio 'datos'
    if not os.path.exists(datos_dir):
        os.makedirs(datos_dir)
        tk.messagebox.showinfo(
            "Directorio creado",
            "Directorio 'datos' no encontrado, se ha creado de nuevo. Asegúrate de añadir los archivos de datos a esta."
        )
        # [!!!] Siento que este return es un crimen, comprobar más tarde
        return  # Si se acaba de crear, no puede haber archivos, por lo que no se molesta en comprobar

    # [!!!] Sustituir......
    # [!!!] Y comprobar que no explote por caracteres especiales....................
    archivos_requeridos = ['regimen_general.xls', 'todas_las_ensenanzas.xls', 'ensenanza_de_adultos.xls']
    archivos_presentes = os.listdir(datos_dir)

    resultado = []

    # Función para buscar el curso en los encabezados
    def encontrar_curso(encabezados):
        for encabezado in encabezados:
            if isinstance(encabezado, str):
                # Obtener el año según patrón
                curso_match = re.search(r'\b\d{4}-\d{4}\b', encabezado)
                if curso_match:
                    return curso_match.group(0)
        return None

    # Bucle de comprobación
    for archivo in archivos_requeridos:
        if archivo in archivos_presentes:
            # ¿Está? Intenta sacar el año de dicho archivo y muestra un tic
            try:
                # [X!!!] Suponiendo que el curso está en la primera fila, primera columna (Revisar......)
                # > Se tenía que sacar del encabezado, no la primera fila/columna. Solucionado.
                df = pd.read_excel(os.path.join(datos_dir, archivo), header=0)
                curso_encontrado = encontrar_curso(df.columns)

                if curso_encontrado:
                    resultado.append((f"✅ {archivo}", f"Curso: {curso_encontrado}"))
                else:
                    resultado.append((f"✅ {archivo}", "Curso no encontrado en el encabezado"))
            except Exception as e:
                # En caso de que de excepción, devolver cruz.
                resultado.append((f"❌ {archivo}", f"Error: {str(e)}"))
        else:
            # ¿No está? devuelve cruz.
            resultado.append((f"❌ {archivo}", "Archivo no encontrado"))

    # Creación de root (ventana)
    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados de Comprobación")

    # --- INTERFAZ GRÁFICA (WIP) ---
    tree = ttk.Treeview(ventana_resultados, columns=("Documento", "Estado"), show="headings")
    tree.heading("Documento", text="Documento")
    tree.heading("Estado", text="Estado")
    tree.pack(expand=True, fill=tk.BOTH)

    for estado, detalle in resultado:
        tree.insert("", "end", values=(estado, detalle))
