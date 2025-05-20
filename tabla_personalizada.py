import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
import re

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
        
        # Lista de tablas seleccionadas
        self.lista_tablas = ttk.Treeview(main_frame, columns=('config',), show='headings', selectmode='browse')
        self.lista_tablas.heading('#0', text='Tabla')
        self.lista_tablas.heading('config', text='Configuración')
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
        tabla = item['text']
        
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
                    for fila in ["01 ANDALUCÍA", "02 ARAGÓN", "03 ASTURIAS"]} 
                    for tabla in self.tablas_disponibles}
        
        # Deshabilitar checkboxes de tablas ya seleccionadas
        tablas_ya_seleccionadas = [t[0] for t in self.tablas_seleccionadas]
        
        # > Antes esto era una lista de botones gigante y lo considero cutre. Me gusta más la idea de varias pestañas        
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
            for i, fila in enumerate(["01 ANDALUCÍA", "02 ARAGÓN", "03 ASTURIAS"]):
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
                    self.lista_tablas.insert('', tk.END, text=tabla, values=(str(config)))
            
            ventana_seleccion.destroy()
        
        ttk.Button(ventana_seleccion, text="Confirmar", command=confirmar).pack(pady=10)
    
    def generar_excel(self):
        if not self.tablas_seleccionadas:
            messagebox.showwarning("Advertencia", "No hay tablas seleccionadas")
            return
        
        # Crear directorio si no existe
        if not os.path.exists('resultados'):
            os.makedirs('resultados')
        
        # Procesar cada tabla seleccionada
        resultados = []
        for tabla, config in self.tablas_seleccionadas:
            try:
                archivo = f"datos/{tabla}.xls"
                df = pd.read_excel(archivo, header=6)
                
                # Limpiar nombres de columnas
                df.columns = [self.limpiar_texto(col) if isinstance(col, str) else col for col in df.columns]
                df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: self.limpiar_texto(x) if isinstance(x, str) else x)
                
                # > Con tanto borrado y cambio se me quedaron variables muertas. Ya no es el caso.
                
                # Procesar cada sección seleccionada
                for seccion in config['secciones']:
                    # Encontrar el índice de la sección
                    idx_seccion = df.index[df.iloc[:, 0] == seccion].tolist()
                    if not idx_seccion:
                        continue  # Si no se encuentra la sección, pasar a la siguiente
                    
                    start_idx = idx_seccion[0]
                    end_idx = start_idx + 1
                    
                    # Buscar el final de la sección (hasta la siguiente sección o fin de dataframe)
                    while end_idx < len(df) and df.iloc[end_idx, 0] not in config['secciones']:
                        end_idx += 1
                    
                    # Extraer solo esta sección
                    df_seccion = df.iloc[start_idx:end_idx].copy()
                    
                    # Procesar cada subsección seleccionada dentro de esta sección
                    for subseccion in config['subsecciones']:
                        # Encontrar el índice de la subsección
                        idx_sub = df_seccion.index[df_seccion.iloc[:, 0] == subseccion].tolist()
                        if not idx_sub:
                            continue  # Si no se encuentra la subsección, pasar a la siguiente
                        
                        start_sub = idx_sub[0]
                        end_sub = start_sub + 1
                        
                        # Buscar el final de la subsección (hasta la siguiente subsección o fin de sección)
                        while (end_sub < len(df_seccion)) and (df_seccion.iloc[end_sub, 0] not in config['subsecciones']):
                            end_sub += 1
                        
                        # Extraer solo esta subsección
                        df_subseccion = df_seccion.iloc[start_sub:end_sub].copy()
                        
                        # Filtrar solo las filas objetivo dentro de esta subsección
                        df_filas = df_subseccion[df_subseccion.iloc[:, 0].isin(config['filas'])].copy()
                        
                        # Si encontramos filas que coinciden, añadirlas a los resultados
                        if not df_filas.empty:
                            df_filas['Tabla'] = tabla
                            df_filas['Sección'] = seccion
                            df_filas['Subsección'] = subseccion
                            resultados.append(df_filas)
            
            except Exception as e:
                messagebox.showerror("Error", f"Error procesando {tabla}:\n{e}")
                return
        
        if resultados:
            # Combinar todos los resultados
            df_final = pd.concat(resultados, ignore_index=True)
            
            # Eliminar columnas duplicadas si las hay
            df_final = df_final.loc[:, ~df_final.columns.duplicated()]
            
            # Guardar el resultado
            archivo_salida = "resultados/tabla_personalizada.xlsx"
            df_final.to_excel(archivo_salida, index=False)
            messagebox.showinfo("Éxito", f"Archivo generado:\n{archivo_salida}")
        else:
            messagebox.showwarning("Advertencia", "No se encontraron datos con los criterios seleccionados")
    
    def limpiar_texto(self, texto):
        if not isinstance(texto, str):
            return texto
        texto = re.sub(r"\s*[\(\[].*?[\)\]]", "", texto)
        texto = re.sub(r"\s*\*.*$", "", texto)
        return texto.strip()
    
    def cerrar(self):
        self.ventana.destroy()
        self.root.deiconify()

def mostrar_menu_personalizadas(root):
    TablaPersonalizada(root)