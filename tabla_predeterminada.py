import tkinter as tk
from tkinter import messagebox
import pandas as pd

def mostrar_menu_predeterminadas(root):
    # Creación de root (ventana)
    ventana_predeterminadas = tk.Toplevel(root)
    ventana_predeterminadas.title("Tablas Predeterminadas")

    # Extraer descripciones pertinentes del archivo csv correspondiente
    try:
        # Encuentra el archivo (encoding="latin-1" para que no de error por no reconocer caracteres en utf-8)
        df_descripciones = pd.read_csv("modelos/descripciones.csv", encoding="latin-1")
        # Toma dos columnas del DataFrame (Tabla y Descripción) y las convierte en un diccionario
        descripciones = dict(zip(df_descripciones['Tabla'], df_descripciones['Descripción']))
    except Exception as e:
        # [!!!] Comprobar qué ocurre con las descripciones en caso de error......
        # [!!!] Debería de poner que no hay
        messagebox.showerror("Error", f"No se pudo cargar el archivo de descripciones:\n{e}")
        return

    # --- INTERFAZ GRÁFICA (WIP) ---
    tablas_predeterminadas = list(descripciones.keys())

    # Crear una nueva ventana que muestre la descripción, regresar y generar xls
    # [!!!] Bastante seguro de que se implementarán más formatos, revisar.
    # [!!!] Nuevamente, ver que no genere mútliples ventanas, solo 1.
    def mostrar_detalle(tabla):
        # Ventana
        ventana_detalle = tk.Toplevel(ventana_predeterminadas)
        ventana_detalle.title(f"Detalle de {tabla}")

        # Descripción
        descripcion = descripciones.get(tabla, "No hay descripción disponible.")
        tk.Label(ventana_detalle, text=descripcion, wraplength=400, justify="left").pack(pady=10)

        # Método para generar xls
        def generar_xls():
            try:
                plantilla = pd.read_excel(f'modelos/{tabla}.xls')
                plantilla.to_excel(f'resultados/{tabla}.xls', index=False)
                messagebox.showinfo("Éxito", f"Tabla {tabla} generada y guardada en Resultados.")
                ventana_detalle.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la tabla:\n{e}")

        # Botones
        tk.Button(ventana_detalle, text="Generar XLS", command=generar_xls).pack(pady=5)
        tk.Button(ventana_detalle, text="Regresar", command=ventana_detalle.destroy).pack(pady=5)

    for tabla in tablas_predeterminadas:
        tk.Button(ventana_predeterminadas, text=tabla, command=lambda t=tabla: mostrar_detalle(t)).pack(pady=5)

    tk.Button(ventana_predeterminadas, text="Regresar", command=ventana_predeterminadas.destroy).pack(pady=5)
