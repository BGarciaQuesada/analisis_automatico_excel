import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import re
from plantilla import ModeloPlantilla

class TablaPersonalizada:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Tablas Personalizadas")
        self.ventana.minsize(800, 600)
        
        # Variables para almacenar selecciones
        self.tablas_seleccionadas = []  # Ahora almacenamos (tabla, config) como diccionario
        self.tablas_disponibles = ["regimen_general", "infantil", "primaria"]
        
        # Interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # > Se ha creado una columna nueva para indicar el nombre de la tabla de la que se cogen los datos (claridez)
        # Lista de tablas seleccionadas
        self.lista_tablas = ttk.Treeview(main_frame, columns=('tabla', 'config'), show='headings', selectmode='browse')
        self.lista_tablas.heading('tabla', text='Tabla')
        self.lista_tablas.heading('config', text='Configuración')
        self.lista_tablas.column('tabla', width=150)
        self.lista_tablas.column('config', width=400)
        self.lista_tablas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.lista_tablas.yview)
        scrollbar.pack(side="right", fill="y")
        self.lista_tablas.configure(yscrollcommand=scrollbar.set)
        
        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Añadir Tabla", command=self.agregar_tabla).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Seleccionado", command=self.eliminar_tabla).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generar Excel", command=self.generar_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Regresar", command=self.cerrar).pack(side=tk.RIGHT, padx=5)
    
    def eliminar_tabla(self):
        seleccion = self.lista_tablas.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una tabla para eliminar")
            return
        
        # Eliminar de la lista visual
        item = self.lista_tablas.item(seleccion[0])
        tabla = item['values'][0]  # Ahora el nombre está en values[0]
        
        # Eliminar de la lista interna
        self.tablas_seleccionadas = [t for t in self.tablas_seleccionadas if t[0] != tabla]
        
        # Eliminar de la vista
        self.lista_tablas.delete(seleccion[0])
    
    def agregar_tabla(self):
        ventana_seleccion = tk.Toplevel(self.ventana)
        ventana_seleccion.title("Seleccionar Tabla")
        ventana_seleccion.minsize(600, 400)
        
        # Variables para almacenar selecciones
        var_secciones = {tabla: {seccion: tk.BooleanVar() 
                        for seccion in ["TODOS LOS CENTROS", "CENTROS PÚBLICOS"]} 
                        for tabla in self.tablas_disponibles}
        
        var_subsecciones = {tabla: {sub: tk.BooleanVar() 
                           for sub in ["AMBOS SEXOS", "Hombres", "Mujeres"]} 
                           for tabla in self.tablas_disponibles}
        
        var_filas = {tabla: {fila: tk.BooleanVar() 
                    for fila in ["01 ANDALUCÍA", "Granada", "02 ARAGÓN"]} 
                    for tabla in self.tablas_disponibles}
        
        # Deshabilitar checkboxes de tablas ya seleccionadas
        tablas_ya_seleccionadas = [t[0] for t in self.tablas_seleccionadas]
                
        # Notebook para organizar las pestañas
        notebook = ttk.Notebook(ventana_seleccion)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        for tabla in self.tablas_disponibles:
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tabla)
            
            # Deshabilitar pestaña si la tabla ya está seleccionada
            if tabla in tablas_ya_seleccionadas:
                notebook.tab(tab_frame, state='disabled')
                ttk.Label(tab_frame, 
                          text=f"La tabla {tabla} ya está seleccionada",
                          foreground='gray').pack(pady=50)
                continue
            
            # Secciones
            ttk.Label(tab_frame, text="Secciones:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
            for i, seccion in enumerate(["TODOS LOS CENTROS", "CENTROS PÚBLICOS"]):
                cb = ttk.Checkbutton(tab_frame, text=seccion, variable=var_secciones[tabla][seccion])
                cb.grid(row=i+1, column=0, sticky=tk.W, padx=20, pady=2)
            
            # Subsecciones
            ttk.Label(tab_frame, text="Subsecciones:").grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
            for i, sub in enumerate(["AMBOS SEXOS", "Hombres", "Mujeres"]):
                cb = ttk.Checkbutton(tab_frame, text=sub, variable=var_subsecciones[tabla][sub])
                cb.grid(row=i+1, column=1, sticky=tk.W, padx=20, pady=2)
            
            # Filas objetivo
            ttk.Label(tab_frame, text="Filas objetivo:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
            for i, fila in enumerate(["01 ANDALUCÍA", "Granada", "02 ARAGÓN"]):
                cb = ttk.Checkbutton(tab_frame, text=fila, variable=var_filas[tabla][fila])
                cb.grid(row=i+1, column=2, sticky=tk.W, padx=20, pady=2)
        
        # Botón para confirmar
        def confirmar():
            for tabla in self.tablas_disponibles:
                if tabla in tablas_ya_seleccionadas:
                    continue  # Saltar tablas ya seleccionadas
                
                secciones = [s for s in var_secciones[tabla] if var_secciones[tabla][s].get()]
                subsecciones = [s for s in var_subsecciones[tabla] if var_subsecciones[tabla][s].get()]
                filas = [f for f in var_filas[tabla] if var_filas[tabla][f].get()]
                
                if secciones and subsecciones and filas:
                    config = {
                        'secciones': secciones,
                        'subsecciones': subsecciones,
                        'filas': filas
                    }
                    self.tablas_seleccionadas.append((tabla, config))
                    self.lista_tablas.insert('', tk.END, values=(tabla, str(config)))
            
            ventana_seleccion.destroy()
        
        ttk.Button(ventana_seleccion, text="Confirmar", command=confirmar).pack(pady=10)
    
    def generar_excel(self):
        if not self.tablas_seleccionadas:
            messagebox.showwarning("Advertencia", "No hay tablas seleccionadas")
            return
        
        # Crear directorio si no existe
        try:
            if not os.path.exists('resultados'):
                os.makedirs('resultados')
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el directorio 'resultados':\n{e}")
            return
        
        # > Me he dado cuenta que no llegué a hacer el cambio de usar ModeloPlantilla aquí. Arreglado.
        # Preparar datos para ModeloPlantilla
        archivos_entrada = []
        secciones = []
        subsecciones = []
        filas_objetivo = []
        
        for tabla, config in self.tablas_seleccionadas:
            archivo = f"datos/{tabla}.xls"
            if not os.path.exists(archivo):
                messagebox.showwarning("Advertencia", f"Archivo no encontrado: {archivo}")
                continue
            
            archivos_entrada.append(archivo)
            secciones.extend(config['secciones'])
            subsecciones.extend(config['subsecciones'])
            filas_objetivo.extend(config['filas'])
        
        if not archivos_entrada:
            messagebox.showwarning("Advertencia", "No hay archivos válidos para procesar")
            return
        
        archivo_salida = "resultados/tabla_personalizada.xlsx"
        
        # Usar ModeloPlantilla para procesar los datos
        modelo = ModeloPlantilla(
            archivos_entrada=archivos_entrada,
            archivo_salida=archivo_salida,
            secciones=secciones,
            subsecciones=subsecciones,
            filas_objetivo=filas_objetivo
        )
        
        modelo.ejecutar_modelo(self.root)
    
    def cerrar(self):
        self.ventana.destroy()
        self.root.deiconify()

def mostrar_menu_personalizadas(root):
    TablaPersonalizada(root)