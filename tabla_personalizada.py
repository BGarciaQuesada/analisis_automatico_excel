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
        # [!!!] Esto va a cambiar de tabla en tabla, WIP.
        def seleccionar_tabla(tabla):
            ventana_configuracion = tk.Toplevel(ventana_seleccion)
            ventana_configuracion.title(f"Configurar {tabla}")

            # Cajas marcables
            opciones_datos = ["género", "cursos", "provincia"]
            var_datos = {opcion: tk.IntVar() for opcion in opciones_datos}

            # Método para saber qué se ha marcado en cada una
            def guardar_configuracion():
                datos_seleccionados = [opcion for opcion, var in var_datos.items() if var.get()]
                if datos_seleccionados:
                    configuracion = {
                        'secciones': ['TODOS LOS CENTROS', 'CENTROS PÚBLICOS'],
                        'subsecciones': datos_seleccionados,
                        'filas_objetivo': ['01 ANDALUCÍA']
                    }
                    tablas_seleccionadas.append((tabla, configuracion))
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

        # Comprobación de la existencia del directorio 'resultados'
        resultados_dir = 'resultados'
        if not os.path.exists(resultados_dir):
            os.makedirs(resultados_dir)
            messagebox.showinfo(
                "Directorio creado",
                "Directorio 'resultados' no encontrado, se ha creado de nuevo. Las tablas personalizadas se guardaran en esta."
            )

        archivos_entrada = [f'datos/{tabla}.xls' for tabla, _ in tablas_seleccionadas]
        archivos_salida = 'resultados/tabla_personalizada.xlsx'
        configuraciones = [config for _, config in tablas_seleccionadas]

        # Usar la primera configuración para secciones, subsecciones y filas_objetivo
        modelo_plantilla = ModeloPlantilla(
            archivos_entrada=archivos_entrada,
            archivos_salida=archivos_salida,
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
