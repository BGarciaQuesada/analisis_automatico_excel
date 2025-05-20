import os
import pandas as pd
import re
import tkinter as tk
from tkinter import ttk, messagebox

def comprobar_datos(root):
    # Ocultar la ventana anterior
    root.withdraw() 

    # Crear ventana con nuevo estilo
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
        messagebox.showinfo(
            "Directorio creado",
            "Directorio 'datos' no encontrado, se ha creado de nuevo. Asegúrate de añadir los archivos de datos a esta."
        )
        return  # Si se acaba de crear, no puede haber archivos, por lo que no se molesta en comprobar

    archivos_requeridos = ['regimen_general.xls', 'todas_las_ensenanzas.xls', 'ensenanza_de_adultos.xls']
    archivos_presentes = os.listdir(datos_dir)

    resultado = []

    # Función para buscar el curso en los encabezados
    def encontrar_curso(encabezados):
        for encabezado in encabezados:
            if isinstance(encabezado, str):
                curso_match = re.search(r'\b\d{4}-\d{4}\b', encabezado)
                if curso_match:
                    return curso_match.group(0)
        return None

    # Bucle de comprobación
    for archivo in archivos_requeridos:
        if archivo in archivos_presentes:
            try:
                df = pd.read_excel(os.path.join(datos_dir, archivo), header=0)
                curso_encontrado = encontrar_curso(df.columns)

                if curso_encontrado:
                    resultado.append((f"✅ {archivo}", f"Curso: {curso_encontrado}"))
                else:
                    resultado.append((f"✅ {archivo}", "Curso no encontrado en el encabezado"))
            except Exception as e:
                resultado.append((f"❌ {archivo}", f"Error: {str(e)}"))
        else:
            resultado.append((f"❌ {archivo}", "Archivo no encontrado"))

    # --- INTERFAZ GRÁFICA ---

    # Treeview con scrollbar
    tree_frame = ttk.Frame(main_frame)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    tree = ttk.Treeview(tree_frame, columns=("Estado"), show="headings")
    tree.heading("#0", text="Documento")
    tree.heading("Estado", text="Estado")
    
    vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    
    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    for estado, detalle in resultado:
        tree.insert("", "end", text=estado, values=(detalle,))
    
    # Botón de Regresar con nuevo estilo
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=10)
    
    ttk.Button(btn_frame, text="Regresar", 
              command=lambda: [ventana_resultados.destroy(), root.deiconify()]).pack(side=tk.RIGHT)