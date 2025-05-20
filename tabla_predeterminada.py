import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import importlib
from plantilla import ModeloPlantilla 

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
        
        # Descripción del modelo
        descripcion = f"Descripción del modelo {modelo}\n\nEste modelo generará una tabla con los datos básicos de {modelo}"
        ttk.Label(detalle_frame, text=descripcion, wraplength=400, justify="left").pack(pady=20)
        
        # Frame para botones
        btn_frame = ttk.Frame(detalle_frame)
        btn_frame.pack(pady=20)
        
        def generar_xls():
            try:
                # Crear una instancia de ModeloPlantilla con los parámetros necesarios
                modelo_plantilla = ModeloPlantilla(
                    archivos_entrada=['datos/regimen_general.xls'],  # Nota: archivos_entrada es una lista
                    archivo_salida=f'resultados/{modelo}.xlsx',
                    secciones=['TODOS LOS CENTROS', 'CENTROS PÚBLICOS'],
                    subsecciones=['AMBOS SEXOS', 'Hombres', 'Mujeres'],
                    filas_objetivo=['01 ANDALUCÍA']
                )
                # Ejecutar el modelo
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