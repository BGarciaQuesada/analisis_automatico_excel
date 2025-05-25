import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import ast  # Necesito esto porque si no los strings no pasan a lista bien
from plantilla import ModeloPlantilla 

# > ANTES ESTO SE HACÍA PASANDOLE DATOS A LO BRUTO, HA CAMBIADO BASTANTE
# > El objetivo es que los lea del CSV para automatizar.
# > Afectado: mostrar_detalle_modelo() y generar_xls()

def mostrar_menu_predeterminadas(root):
    # Ocultar la ventana anterior
    root.withdraw()
    
    # Creación de ventana con nuevo estilo
    ventana_predeterminadas = tk.Toplevel(root)
    ventana_predeterminadas.title("Tablas Predeterminadas")
    ventana_predeterminadas.minsize(600, 400)
    
    # Frame principal
    main_frame = ttk.Frame(ventana_predeterminadas)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Título
    ttk.Label(main_frame, text="Selecciona un modelo predeterminado", 
             font=('Arial', 12, 'bold')).pack(pady=10)

    # Asegurarse de que el directorio 'resultados' exista
    if not os.path.exists('resultados'):
        os.makedirs('resultados')
        messagebox.showinfo(
            "Directorio creado",
            "Directorio 'resultados' no encontrado, se ha creado de nuevo. Las tablas predeterminadas se guardaran en esta."
        )

    # Cargar modelos desde CSV
    try:
        modelos_df = pd.read_csv('modelos/modelos_config.csv')
        modelos_disponibles = modelos_df['nombre_modelo'].tolist()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo de configuración:\n{e}")
        modelos_disponibles = []

    # Frame para los botones de modelos
    modelos_frame = ttk.Frame(main_frame)
    modelos_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # --- INTERFAZ GRÁFICA ---
    
    def mostrar_detalle_modelo(modelo):
        # Ventana de detalle
        ventana_detalle = tk.Toplevel(ventana_predeterminadas)
        ventana_detalle.title(f"Modelo: {modelo}")
        ventana_detalle.minsize(500, 300)
        
        # Frame principal
        detalle_frame = ttk.Frame(ventana_detalle)
        detalle_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Obtener parámetros desde CSV
        try:
            config = modelos_df[modelos_df['nombre_modelo'] == modelo].iloc[0]
            archivos_entrada = ast.literal_eval(config['archivos_entrada'])
            secciones = ast.literal_eval(config['secciones'])
            subsecciones = ast.literal_eval(config['subsecciones'])
            filas_objetivo = ast.literal_eval(config['filas_objetivo'])
        except Exception as e:
            messagebox.showerror("Error", f"Configuración inválida para {modelo}:\n{e}")
            return

        # Descripción del modelo (modificado para mostrar info del CSV)
        descripcion = f"Configuración del modelo {modelo}\n\n"
        descripcion += f"· Archivos: {', '.join(archivos_entrada)}\n"
        descripcion += f"· Secciones: {', '.join(secciones)}\n"
        descripcion += f"· Subsecciones: {', '.join(subsecciones)}\n"
        descripcion += f"· Filas: {', '.join(filas_objetivo)}"
        
        ttk.Label(detalle_frame, text=descripcion, wraplength=400, justify="left").pack(pady=20)
        
        # Frame para botones
        btn_frame = ttk.Frame(detalle_frame)
        btn_frame.pack(pady=20)
        
        def generar_xls():
            try:
                # Usar parámetros del CSV
                modelo_plantilla = ModeloPlantilla(
                    archivos_entrada=archivos_entrada,
                    archivo_salida=f'resultados/{modelo}.xlsx',
                    secciones=secciones,
                    subsecciones=subsecciones,
                    filas_objetivo=filas_objetivo
                )
                modelo_plantilla.ejecutar_modelo(ventana_detalle)
                ventana_detalle.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar la tabla:\n{e}")

        ttk.Button(btn_frame, text="Generar XLS", command=generar_xls, width=15).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Regresar", command=ventana_detalle.destroy, width=15).pack(side=tk.RIGHT, padx=10)

    # Crear botones para cada modelo disponible
    for modelo in modelos_disponibles:
        btn_modelo = ttk.Button(
            modelos_frame, 
            text=modelo, 
            command=lambda m=modelo: mostrar_detalle_modelo(m),
            width=30
        )
        btn_modelo.pack(pady=5, fill=tk.X)

    # Botón de Regresar
    ttk.Button(
        main_frame, 
        text="Regresar", 
        command=lambda: [ventana_predeterminadas.destroy(), root.deiconify()],
        width=20
    ).pack(pady=20)