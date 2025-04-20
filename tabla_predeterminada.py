import tkinter as tk
from tkinter import messagebox
import pandas as pd

def mostrar_menu_predeterminadas(root):
    ventana_predeterminadas = tk.Toplevel(root)
    ventana_predeterminadas.title("Tablas Predeterminadas")

    tablas_predeterminadas = ["Tabla 2.10", "Tabla 2.15", "Tabla 2.27"]

    def mostrar_detalle(tabla):
        ventana_detalle = tk.Toplevel(ventana_predeterminadas)
        ventana_detalle.title(f"Detalle de {tabla}")

        tk.Label(ventana_detalle, text=f"Descripción general de {tabla}").pack(pady=10)

        def generar_xls():
            # Lógica para generar el XLS
            plantilla = pd.read_excel(f'Modelos/{tabla}.xls')
            plantilla.to_excel(f'Resultados/{tabla}.xls', index=False)
            messagebox.showinfo("Éxito", f"Tabla {tabla} generada y guardada en Resultados.")
            ventana_detalle.destroy()

        tk.Button(ventana_detalle, text="Generar XLS", command=generar_xls).pack(pady=5)
        tk.Button(ventana_detalle, text="Regresar", command=ventana_detalle.destroy).pack(pady=5)

    for tabla in tablas_predeterminadas:
        tk.Button(ventana_predeterminadas, text=tabla, command=lambda t=tabla: mostrar_detalle(t)).pack(pady=5)

    tk.Button(ventana_predeterminadas, text="Regresar", command=ventana_predeterminadas.destroy).pack(pady=5)
