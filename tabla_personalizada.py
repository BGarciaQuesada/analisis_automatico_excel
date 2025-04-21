import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

def mostrar_menu_personalizadas(root):
    # Crear root (ventana)
    ventana_personalizadas = tk.Toplevel(root)
    ventana_personalizadas.title("Tablas Personalizadas")

    tablas_disponibles = ["regimen_general", "infantil", "primaria"]
    tablas_seleccionadas = []

    # --- INTERFAZ GRÁFICA (WIP) ---

    # Lista donde se agregan las tablas a juntar
    def agregar_tabla():
        ventana_seleccion = tk.Toplevel(ventana_personalizadas)
        ventana_seleccion.title("Seleccionar Tabla")

        # Al seleccionar una tabla, mostrar las casillas a marcar
        # [!!!] Esto va a cambiar de tabla en tabla, WIP.
        def seleccionar_tabla(tabla):
            ventana_configuracion = tk.Toplevel(ventana_seleccion)
            ventana_configuracion.title(f"Configurar {tabla}")

            # Cajas marcables
            opciones_datos = ["género", "cursos", "provincia"]
            var_datos = {opcion: tk.IntVar() for opcion in opciones_datos}

            # Métododo para saber qué se ha marcado en cada una
            def guardar_configuracion():
                datos_seleccionados = [opcion for opcion, var in var_datos.items() if var.get()]
                if datos_seleccionados:
                    tablas_seleccionadas.append((tabla, datos_seleccionados))
                    listbox_tablas.insert(tk.END, f"{tabla} ({', '.join(datos_seleccionados)})")
                ventana_configuracion.destroy()
                ventana_seleccion.destroy()

            for opcion in opciones_datos:
                tk.Checkbutton(ventana_configuracion, text=opcion, variable=var_datos[opcion]).pack(anchor=tk.W)

            tk.Button(ventana_configuracion, text="Guardar", command=guardar_configuracion).pack(pady=5)

        for tabla in tablas_disponibles:
            tk.Button(ventana_seleccion, text=tabla, command=lambda t=tabla: seleccionar_tabla(t)).pack(pady=5)

    # Método para generar xls
    # [!!!] ¿Y cómo juntarrremos las tablas? La rrrespuesta es clarrra. No lo harrremos.
    # [!!!] Hablando en serio, hay que analizar eso.
    def generar_xls():
        if not tablas_seleccionadas:
            messagebox.showwarning("Advertencia", "Debes seleccionar al menos una tabla.")
            return

        for tabla, datos in tablas_seleccionadas:
            df = pd.DataFrame(columns=datos)
            df.to_excel(f'resultados/{tabla}_personalizada.xls', index=False)

        messagebox.showinfo("Éxito", "Tabla personalizada generada y guardada en Resultados.")
        ventana_personalizadas.destroy()

    listbox_tablas = tk.Listbox(ventana_personalizadas)
    listbox_tablas.pack(pady=10)

    # Botones
    tk.Button(ventana_personalizadas, text="+", command=agregar_tabla).pack(pady=5)
    tk.Button(ventana_personalizadas, text="Generar XLS", command=generar_xls).pack(pady=5)
    tk.Button(ventana_personalizadas, text="Regresar", command=ventana_personalizadas.destroy).pack(pady=5)
