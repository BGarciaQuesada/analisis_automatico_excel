import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import importlib

def mostrar_menu_predeterminadas(root):
    # Creación de root (ventana)
    ventana_predeterminadas = tk.Toplevel(root)
    ventana_predeterminadas.title("Tablas Predeterminadas")

    # Asegurarse de que el directorio 'resultados' exista
    if not os.path.exists('resultados'):
        os.makedirs('resultados')

    # Detectar modelos disponibles en la carpeta 'modelos'
    modelos_dir = 'modelos'
    modelos_disponibles = [f.replace('.py', '') for f in os.listdir(modelos_dir) if f.endswith('.py')]

    # --- INTERFAZ GRÁFICA (WIP) ---
    def mostrar_detalle(modelo):
        ventana_detalle = tk.Toplevel(ventana_predeterminadas)
        ventana_detalle.title(f"Detalle de {modelo}")

        descripcion = f"Descripción del modelo {modelo}"
        tk.Label(ventana_detalle, text=descripcion, wraplength=400, justify="left").pack(pady=10)

        def generar_xls():
            try:
                # Importar dinámicamente el módulo del modelo
                modulo = importlib.import_module(f"modelos.{modelo}")
                modulo.ejecutar_modelo(ventana_detalle)
                messagebox.showinfo("Éxito", f"Tabla {modelo} generada y guardada en Resultados.")
                ventana_detalle.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la tabla:\n{e}")

        tk.Button(ventana_detalle, text="Generar XLS", command=generar_xls).pack(pady=5)
        tk.Button(ventana_detalle, text="Regresar", command=ventana_detalle.destroy).pack(pady=5)

    for modelo in modelos_disponibles:
        tk.Button(ventana_predeterminadas, text=modelo, command=lambda m=modelo: mostrar_detalle(m)).pack(pady=5)

    tk.Button(ventana_predeterminadas, text="Regresar", command=ventana_predeterminadas.destroy).pack(pady=5)
