import pandas as pd
import re
import os
import tkinter as tk
from tkinter import messagebox

class ModeloPlantilla:
    def __init__(self, archivos_entrada, archivos_salida, secciones, subsecciones, filas_objetivo):
        self.archivos_entrada = archivos_entrada
        self.archivos_salida = archivos_salida
        self.secciones = secciones  # Lista de secciones a buscar
        self.subsecciones = subsecciones  # Lista de subsecciones a buscar
        self.filas_objetivo = filas_objetivo  # Lista de filas objetivo a extraer

    def limpiar_titulo(self, titulo):
        titulo = re.sub(r"\s*[\(\[].*?[\)\]]", "", titulo)
        titulo = re.sub(r"\s*\*.*$", "", titulo)
        titulo = titulo.strip()
        return titulo

    def ejecutar_modelo(self, root):
        # Asegurarse de que el directorio 'datos' exista
        if not os.path.exists('datos'):
            os.makedirs('datos')
            messagebox.showinfo("Información", f"El directorio 'datos' no existía y fue creado. Por favor, coloca el archivo '{self.archivos_entrada}' en esa carpeta.")
            return

        try:
            # Cargar el Excel CON ENCABEZADOS desde la fila 7
            df = pd.read_excel(self.archivos_entrada, header=6)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo '{self.archivos_entrada}':\n{e}")
            return

        # Limpieza de títulos de columnas
        df.columns = [self.limpiar_titulo(col) if isinstance(col, str) else col for col in df.columns]

        # Limpieza de títulos de la primera columna
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: self.limpiar_titulo(x.strip()) if isinstance(x, str) else x)

        # Encontrar índices de las secciones
        secciones_indices = {seccion: df[df.iloc[:, 0] == seccion].index for seccion in self.secciones}

        if any(index.empty for index in secciones_indices.values()):
            messagebox.showerror("Error", "No se encontraron todas las secciones necesarias.")
            return

        # Filtrar la sección desde la primera sección hasta la última sección
        df_seccion = df.iloc[secciones_indices[self.secciones[0]][0]:secciones_indices[self.secciones[1]][0]]

        # Encontrar índices dentro de la sección filtrada para las subsecciones
        subsecciones_indices = {subseccion: df_seccion[df_seccion.iloc[:, 0] == subseccion].index for subseccion in self.subsecciones}

        if any(index.empty for index in subsecciones_indices.values()):
            messagebox.showerror("Error", "No se encontraron todas las subsecciones necesarias.")
            return

        # Extraer filas objetivo en cada subsección
        df_final = pd.DataFrame()  # DataFrame para almacenar los resultados

        for i in range(len(self.subsecciones) - 1):
            df_subseccion = df_seccion.iloc[subsecciones_indices[self.subsecciones[i]][0]:subsecciones_indices[self.subsecciones[i+1]][0]]
            df_final = pd.concat([df_final, df_subseccion[df_subseccion.iloc[:, 0].isin(self.filas_objetivo)]])

        # Desde la última subsección hasta el final de la sección
        df_subseccion = df_seccion.iloc[subsecciones_indices[self.subsecciones[-1]][0]:]
        df_final = pd.concat([df_final, df_subseccion[df_subseccion.iloc[:, 0].isin(self.filas_objetivo)]])

        # Guardar el resultado en un archivo Excel
        df_final.to_excel(self.archivos_salida, index=True)

        messagebox.showinfo("Éxito", f"Tabla generada y guardada en {self.archivos_salida}.")
        