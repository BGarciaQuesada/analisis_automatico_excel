import pandas as pd
import re
import os
import tkinter as tk
from tkinter import messagebox

class ModeloPlantilla:
    def __init__(self, archivos_entrada, archivo_salida, secciones, subsecciones, filas_objetivo):
        self.archivos_entrada = archivos_entrada  # Lista de archivos de entrada
        self.archivo_salida = archivo_salida
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
            messagebox.showinfo("Información", f"El directorio 'datos' no existía y fue creado. Por favor, coloca los archivos en esa carpeta.")
            return

        df_final = pd.DataFrame()  # DataFrame para almacenar los resultados

        for archivo in self.archivos_entrada:
            try:
                # Cargar el Excel CON ENCABEZADOS desde la fila 7
                df = pd.read_excel(archivo, header=6)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo '{archivo}':\n{e}")
                return

            # Limpieza de títulos de columnas
            df.columns = [self.limpiar_titulo(col) if isinstance(col, str) else col for col in df.columns]

            # Limpieza de títulos de la primera columna
            df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: self.limpiar_titulo(x.strip()) if isinstance(x, str) else x)

            # Encontrar índices de las secciones
            secciones_indices = {seccion: df[df.iloc[:, 0] == seccion].index for seccion in self.secciones}

            if any(index.empty for index in secciones_indices.values()):
                messagebox.showerror("Error", f"No se encontraron todas las secciones necesarias en el archivo {archivo}.")
                return

            # Filtrar la sección desde la primera sección hasta el final del archivo
            df_seccion = df.iloc[secciones_indices[self.secciones[0]][0]:]

            # Encontrar índices dentro de la sección filtrada para las subsecciones
            subsecciones_indices = {subseccion: df_seccion[df_seccion.iloc[:, 0] == subseccion].index for subseccion in self.subsecciones}

            if any(index.empty for index in subsecciones_indices.values()):
                messagebox.showerror("Error", f"No se encontraron todas las subsecciones necesarias en el archivo {archivo}.")
                return

            # Extraer filas objetivo en cada subsección
            for subseccion in self.subsecciones:
                start_idx = subsecciones_indices[subseccion][0]
                end_idx = start_idx + 1  # Asumimos que cada subsección tiene al menos una fila de datos
                while end_idx < len(df_seccion) and df_seccion.iloc[end_idx, 0] not in self.subsecciones:
                    end_idx += 1
                
                df_subseccion = df_seccion.iloc[start_idx:end_idx]

                # Filtrar filas que coincidan con las filas objetivo
                df_filtrado = df_subseccion[df_subseccion.iloc[:, 0].isin(self.filas_objetivo)]

                # Solo agregar si hay coincidencias
                if not df_filtrado.empty:
                    df_final = pd.concat([df_final, df_filtrado])

        # Guardar el resultado en un archivo Excel
        df_final.to_excel(self.archivo_salida, index=True)

        messagebox.showinfo("Éxito", f"Tabla generada y guardada en {self.archivo_salida}.")
