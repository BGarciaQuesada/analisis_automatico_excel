import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import importlib
from plantilla import ModeloPlantilla  # Asegúrate de que la ruta de importación sea correcta

def mostrar_menu_predeterminadas(root):
    # Ocultar la ventana anterior
    root.withdraw()
    
    # Creación de root (ventana)
    ventana_predeterminadas = tk.Toplevel(root)
    ventana_predeterminadas.title("Tablas Predeterminadas")
    ventana_predeterminadas.minsize(600, 400)  # Tamaño mínimo de la ventana

    # Asegurarse de que el directorio 'resultados' exista
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
        messagebox.showinfo(
            "Directorio creado",
            "Directorio 'resultados' no encontrado, se ha creado de nuevo. Las tablas predeterminadas se guardaran en esta."
        )

    modelos_dir = 'modelos'
    # Comprobación de la existencia del directorio 'modelos'
    if not os.path.exists(modelos_dir):
        os.makedirs(modelos_dir)
        tk.messagebox.showinfo(
            "Directorio creado",
            "Directorio 'modelos' no encontrado, se ha creado de nuevo. Asegúrate de añadir los archivos de modelos a esta."
        )
        return  # Si se acaba de crear, no puede haber archivos, por lo que no se molesta en comprobar

    # Detectar modelos disponibles en la carpeta 'modelos'
    modelos_disponibles = [f.replace('.py', '') for f in os.listdir(modelos_dir) if f.endswith('.py')]

    # --- INTERFAZ GRÁFICA (WIP) ---
    def mostrar_detalle(modelo):
        ventana_detalle = tk.Toplevel(ventana_predeterminadas)
        ventana_detalle.title(f"Detalle de {modelo}")

        descripcion = f"Descripción del modelo {modelo}"
        tk.Label(ventana_detalle, text=descripcion, wraplength=400, justify="left").pack(pady=10)

        def generar_xls():
            try:
                # Crear una instancia de ModeloPlantilla con los parámetros necesarios.
                # Habrá que encontrar una forma de sustuirlos automáticamente más tarde
                # > ¿Guardarlo en un csv?
                modelo_plantilla = ModeloPlantilla(
                    archivos_entrada='datos/regimen_general.xls',
                    archivos_salida=f'resultados/{modelo}.xlsx',
                    secciones=['TODOS LOS CENTROS', 'CENTROS PÚBLICOS'],
                    subsecciones=['AMBOS SEXOS', 'Hombres', 'Mujeres'],
                    filas_objetivo=['01 ANDALUCÍA']
                )
                # Ejecutar el modelo
                modelo_plantilla.ejecutar_modelo(ventana_detalle)
                ventana_detalle.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la tabla:\n{e}")

        tk.Button(ventana_detalle, text="Generar XLS", command=generar_xls).pack(pady=5)
        tk.Button(ventana_detalle, text="Regresar", command=ventana_detalle.destroy).pack(pady=5)

    for modelo in modelos_disponibles:
        tk.Button(ventana_predeterminadas, text=modelo, command=lambda m=modelo: mostrar_detalle(m)).pack(pady=5)

    # Botón de Regresar
    tk.Button(ventana_predeterminadas, text="Regresar", command=lambda: [ventana_predeterminadas.destroy(), root.deiconify()]).pack(pady=10, padx=20, fill=tk.BOTH)
