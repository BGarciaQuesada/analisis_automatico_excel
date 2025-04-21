import tkinter as tk
from tkinter import messagebox
import pandas as pd

def mostrar_menu_predeterminadas(root):
    ventana_predeterminadas = tk.Toplevel(root)
    ventana_predeterminadas.title("Tablas Predeterminadas")

    try:
        df_descripciones = pd.read_csv("modelos/descripciones.csv", encoding="latin-1")
        # Toma dos columnas del DataFrame (Tabla y Descripción) y las convierte en un diccionario
        descripciones = dict(zip(df_descripciones['Tabla'], df_descripciones['Descripción']))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo de descripciones:\n{e}")
        return

    tablas_predeterminadas = list(descripciones.keys())

    def mostrar_detalle(tabla):
        ventana_detalle = tk.Toplevel(ventana_predeterminadas)
        ventana_detalle.title(f"Detalle de {tabla}")

        descripcion = descripciones.get(tabla, "No hay descripción disponible.")
        tk.Label(ventana_detalle, text=descripcion, wraplength=400, justify="left").pack(pady=10)

        def generar_xls():
            try:
                plantilla = pd.read_excel(f'modelos/{tabla}.xls')
                plantilla.to_excel(f'resultados/{tabla}.xls', index=False)
                messagebox.showinfo("Éxito", f"Tabla {tabla} generada y guardada en Resultados.")
                ventana_detalle.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la tabla:\n{e}")

        tk.Button(ventana_detalle, text="Generar XLS", command=generar_xls).pack(pady=5)
        tk.Button(ventana_detalle, text="Regresar", command=ventana_detalle.destroy).pack(pady=5)

    for tabla in tablas_predeterminadas:
        tk.Button(ventana_predeterminadas, text=tabla, command=lambda t=tabla: mostrar_detalle(t)).pack(pady=5)

    tk.Button(ventana_predeterminadas, text="Regresar", command=ventana_predeterminadas.destroy).pack(pady=5)
