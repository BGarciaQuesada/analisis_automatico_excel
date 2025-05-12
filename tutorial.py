import tkinter as tk

# [!!!] Ahora mismo esto es un tochaco de texto. Pretendo sustituirlo luego con imagenes.

def mostrar_tutorial(root):
    # Ocultar la ventana anterior
    root.withdraw()

    ventana_tutorial = tk.Toplevel(root)
    ventana_tutorial.title("Tutorial")
    ventana_tutorial.minsize(600, 400) # Tamaño mínimo de la ventana

    tutorial_text = """
    Bienvenido al Gestor de Tablas MFYP.

    Instrucciones:
    1. Descarga las tablas de la página oficial de MFYP en formato .xls.
    2. Guarda los archivos en la carpeta 'Datos' con los siguientes nombres:
       - regimen_general.xls
       - todas_las_ensenanzas.xls
       - ensenanza_de_adultos.xls
    3. Utiliza el menú principal para comprobar datos, crear tablas predeterminadas o personalizadas.

    Funcionalidades:
    - Comprobación de Datos: Verifica que los archivos necesarios están presentes y muestra el curso.
    - Tabla Predeterminada: Crea una tabla predeterminada basada en una plantilla.
    - Tabla Personalizada: Crea una tabla personalizada según tus especificaciones.
    - Tutorial: Muestra este mensaje de ayuda.
    """

    tk.Label(ventana_tutorial, text=tutorial_text, justify=tk.LEFT).pack(pady=10)
    
    # Botón de Regresar
    tk.Button(ventana_tutorial, text="Regresar", command=lambda: [ventana_tutorial.destroy(), root.deiconify()]).pack(pady=10, padx=20, fill=tk.BOTH)
