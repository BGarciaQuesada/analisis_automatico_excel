import os
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk

def comprobar_datos(root):
    # Ocultar la ventana anterior
    root.withdraw() 

    ventana_resultados = tk.Toplevel(root)
    ventana_resultados.title("Resultados de Comprobación")
    ventana_resultados.minsize(800, 600)
    
    # Frame principal
    main_frame = ttk.Frame(ventana_resultados)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    datos_dir = 'datos'

    # Comprobación de la existencia del directorio 'datos'
    if not os.path.exists(datos_dir):
        os.makedirs(datos_dir)
        tk.messagebox.showinfo(
            "Directorio creado",
            "Directorio 'datos' no encontrado, se ha creado de nuevo. Asegúrese de añadir los archivos de datos a esta."
        )
        return # Si se acaba de crear, no puede haber archivos, por lo que no se molesta en comprobar

    archivos_requeridos = ['regimen_general.xls', 'infantil.xls', 'primaria.xls']
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
            try:
                # Leer el archivo manteniendo el nombre original
                df = pd.read_excel(os.path.join(datos_dir, archivo), header=0)
                curso_encontrado = encontrar_curso(df.columns)

                if curso_encontrado:
                    # > Formato: (nombre_archivo, estado, detalle)
                    resultado.append((archivo, "✅", f"Curso: {curso_encontrado}"))
                else:
                    resultado.append((archivo, "✅", "Archivo válido (curso no detectado)"))
            except Exception as e:
                resultado.append((archivo, "❌", f"Error: {str(e)}"))
        else:
            resultado.append((archivo, "❌", "No encontrado"))

    # --- INTERFAZ GRÁFICA ---

    # Treeview (3 columnas)
    tree = ttk.Treeview(main_frame, columns=("archivo", "estado", "detalle"), show="headings")
    
    # Configurar columnas
    tree.heading("archivo", text="Archivo")
    tree.heading("estado", text="Estado")
    tree.heading("detalle", text="Detalle")
    
    # Ajustar anchos de columna
    tree.column("archivo", width=200, anchor="w")
    tree.column("estado", width=50, anchor="center")
    tree.column("detalle", width=400, anchor="w")
    
    tree.pack(expand=True, fill=tk.BOTH, pady=10)

    # Scrollbar
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # Insertar datos
    for item in resultado:
        tree.insert("", "end", values=item)

    # Botón de Regresar
    ttk.Button(main_frame, text="Regresar", 
              command=lambda: [ventana_resultados.destroy(), root.deiconify()]).pack(pady=10)