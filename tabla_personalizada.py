import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
from plantilla import ModeloPlantilla

# [!!!] CUANDO SE CIERRA EL PROGRAMA DESDE CUALQUIER VENTANA QUE NO SEA LA MAIN NO SE MATA AL PROGRAMA!!!!!!!!!
# [!!!] Es una tontería, ver ahora

#  No se encuentra el archivo. Investigar mañana.

def mostrar_menu_personalizadas(root):
    # Ocultar la ventana anterior
    root.withdraw()

    # Crear root (ventana)
    ventana_personalizadas = tk.Toplevel(root)
    ventana_personalizadas.title("Tablas Personalizadas")
    ventana_personalizadas.minsize(600, 400)  # Tamaño mínimo de la ventana

    tablas_disponibles = ["regimen_general", "infantil", "primaria"]
    tablas_seleccionadas = []

    # --- INTERFAZ GRÁFICA (WIP) ---

    # Lista donde se agregan las tablas a juntar
    def agregar_tabla():
        ventana_seleccion = tk.Toplevel(ventana_personalizadas)
        ventana_seleccion.title("Seleccionar Tabla")

        # Al seleccionar una tabla, mostrar las casillas a marcar
        def seleccionar_tabla(tabla):
            ventana_configuracion = tk.Toplevel(ventana_seleccion)
            ventana_configuracion.title(f"Configurar {tabla}")

            # Cajas marcables para secciones
            opciones_secciones = ["TODOS LOS CENTROS", "CENTROS PÚBLICOS"]
            var_secciones = {opcion: tk.IntVar() for opcion in opciones_secciones}

            # Cajas marcables para subsecciones
            opciones_subsecciones = ["AMBOS SEXOS", "Hombres", "Mujeres"]
            var_subsecciones = {opcion: tk.IntVar() for opcion in opciones_subsecciones}

            # Cajas marcables para filas objetivo
            opciones_filas = ["01 ANDALUCÍA", "02 ARAGÓN", "03 ASTURIAS"]
            var_filas = {opcion: tk.IntVar() for opcion in opciones_filas}

            # Método para saber qué se ha marcado en cada una
            def guardar_configuracion():
                secciones_seleccionadas = [opcion for opcion, var in var_secciones.items() if var.get()]
                subsecciones_seleccionadas = [opcion for opcion, var in var_subsecciones.items() if var.get()]
                filas_seleccionadas = [opcion for opcion, var in var_filas.items() if var.get()]

                if secciones_seleccionadas and subsecciones_seleccionadas and filas_seleccionadas:
                    configuracion = {
                        'secciones': secciones_seleccionadas,
                        'subsecciones': subsecciones_seleccionadas,
                        'filas_objetivo': filas_seleccionadas
                    }
                    tablas_seleccionadas.append((tabla, configuracion))
                    listbox_tablas.insert(tk.END, f"{tabla} (Secciones: {', '.join(secciones_seleccionadas)}, Subsecciones: {', '.join(subsecciones_seleccionadas)}, Filas: {', '.join(filas_seleccionadas)})")
                ventana_configuracion.destroy()
                ventana_seleccion.destroy()

            tk.Label(ventana_configuracion, text="Secciones:").pack(anchor=tk.W)
            for opcion in opciones_secciones:
                tk.Checkbutton(ventana_configuracion, text=opcion, variable=var_secciones[opcion]).pack(anchor=tk.W)

            tk.Label(ventana_configuracion, text="Subsecciones:").pack(anchor=tk.W)
            for opcion in opciones_subsecciones:
                tk.Checkbutton(ventana_configuracion, text=opcion, variable=var_subsecciones[opcion]).pack(anchor=tk.W)

            tk.Label(ventana_configuracion, text="Filas Objetivo:").pack(anchor=tk.W)
            for opcion in opciones_filas:
                tk.Checkbutton(ventana_configuracion, text=opcion, variable=var_filas[opcion]).pack(anchor=tk.W)

            tk.Button(ventana_configuracion, text="Guardar", command=guardar_configuracion).pack(pady=5)

        for tabla in tablas_disponibles:
            tk.Button(ventana_seleccion, text=tabla, command=lambda t=tabla: seleccionar_tabla(t)).pack(pady=5)

    # Método para generar xls
    def generar_xls():
        if not tablas_seleccionadas:
            messagebox.showwarning("Advertencia", "Debes seleccionar al menos una tabla.")
            return

        # Comprobación de la existencia del directorio 'resultados'
        resultados_dir = 'resultados'
        if not os.path.exists(resultados_dir):
            os.makedirs(resultados_dir)
            messagebox.showinfo(
                "Directorio creado",
                "Directorio 'resultados' no encontrado, se ha creado de nuevo. Las tablas personalizadas se guardaran en esta."
            )

        archivos_entrada = [f'datos/{tabla}.xls' for tabla, _ in tablas_seleccionadas]
        archivo_salida = 'resultados/tabla_personalizada.xlsx'
        configuraciones = [config for _, config in tablas_seleccionadas]

        # Usar la primera configuración para secciones, subsecciones y filas_objetivo
        modelo_plantilla = ModeloPlantilla(
            archivos_entrada=archivos_entrada,
            archivo_salida=archivo_salida,
            secciones=configuraciones[0]['secciones'],
            subsecciones=configuraciones[0]['subsecciones'],
            filas_objetivo=configuraciones[0]['filas_objetivo']
        )
        modelo_plantilla.ejecutar_modelo(ventana_personalizadas)

    # Lista
    listbox_tablas = tk.Listbox(ventana_personalizadas, height=15)  # Vertical
    listbox_tablas.pack(pady=10, padx=20, fill=tk.X, expand=False) # Horizontal (Expansión)

    # Botones
    tk.Button(ventana_personalizadas, text="+", command=agregar_tabla).pack(pady=5, padx=20, fill=tk.BOTH)
    tk.Button(ventana_personalizadas, text="Generar XLS", command=generar_xls).pack(pady=5, padx=20, fill=tk.BOTH)

    # Botón de Regresar
    tk.Button(ventana_personalizadas, text="Regresar", command=lambda: [ventana_personalizadas.destroy(), root.deiconify()]).pack(pady=5, padx=20, fill=tk.BOTH)
