import tkinter as tk
from tkinter import ttk

# [!!!] Ahora mismo esto es un tochaco de texto. Pretendo sustituirlo luego con imagenes.

def mostrar_tutorial(root):
    # Ocultar la ventana anterior
    root.withdraw()

    # Crear ventana con nuevo estilo
    ventana_tutorial = tk.Toplevel(root)
    ventana_tutorial.title("Tutorial")
    ventana_tutorial.minsize(800, 600)
    
    # Frame principal
    main_frame = ttk.Frame(ventana_tutorial)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Texto del tutorial con scrollbar
    texto_frame = ttk.Frame(main_frame)
    texto_frame.pack(fill=tk.BOTH, expand=True)
    
    texto = tk.Text(texto_frame, wrap=tk.WORD, font=('Arial', 11))
    vsb = ttk.Scrollbar(texto_frame, orient="vertical", command=texto.yview)
    texto.configure(yscrollcommand=vsb.set)
    
    texto.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    
    texto_frame.grid_rowconfigure(0, weight=1)
    texto_frame.grid_columnconfigure(0, weight=1)
    
    tutorial_text = """
    Bienvenido al Gestor de Tablas MFYP.

    Instrucciones:
    1. Descarga las tablas de la página oficial de MFYP en formato .xls.
    2. Guarda los archivos en la carpeta 'Datos' con los siguientes nombres:
       - regimen_general.xls
       - todas_las_ensenanzas.xls
       - ensenanza_de_adultos.xls
    3. Utiliza el menú principal para:
       - Comprobar datos: Verifica archivos y muestra el curso
       - Crear tablas predeterminadas: Basadas en plantillas
       - Crear tablas personalizadas: Según tus especificaciones
       - Ver este tutorial: Mensaje de ayuda

    Consejos:
    - Verifica siempre que los archivos tienen el formato correcto
    - Si hay errores, revisa los nombres de los archivos
    - Las tablas personalizadas permiten combinar múltiples criterios
    """
    
    texto.insert(tk.END, tutorial_text)
    texto.config(state=tk.DISABLED)
    
    # Botón de Regresar con nuevo estilo
    btn_frame = ttk.Frame(main_frame)
    btn_frame.pack(fill=tk.X, pady=10)
    
    ttk.Button(btn_frame, text="Regresar", 
              command=lambda: [ventana_tutorial.destroy(), root.deiconify()]).pack(side=tk.RIGHT)