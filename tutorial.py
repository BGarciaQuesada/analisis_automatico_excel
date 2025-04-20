import tkinter as tk

def mostrar_tutorial(root):
    ventana_tutorial = tk.Toplevel(root)
    ventana_tutorial.title("Tutorial")

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
    tk.Button(ventana_tutorial, text="Cerrar", command=ventana_tutorial.destroy).pack(pady=5)
