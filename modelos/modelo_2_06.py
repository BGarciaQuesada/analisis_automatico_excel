import pandas as pd
import re
import os
import tkinter as tk
from tkinter import messagebox

def limpiar_titulo(titulo):
    titulo = re.sub(r"\s*[\(\[].*?[\)\]]", "", titulo)
    titulo = re.sub(r"\s*\*.*$", "", titulo)
    titulo = titulo.strip()
    return titulo

def ejecutar_modelo(root):
    # Asegurarse de que el directorio 'datos' exista
    if not os.path.exists('datos'):
        messagebox.showerror("Error", "El directorio 'datos' no existe.")
        return

    try:
        # Cargar el Excel con encabezados desde la fila 7
        df = pd.read_excel('datos/regimen_general.xls', header=6)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo 'regimen_general.xls':\n{e}")
        return

    # Limpieza de títulos de columnas
    df.columns = [limpiar_titulo(col) if isinstance(col, str) else col for col in df.columns]

    # Limpieza de títulos de la primera columna
    df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: limpiar_titulo(x) if isinstance(x, str) else x)

    # Datos a encontrar
    columnas_objetivo = ['TOTAL', 'E. Infantil - Primer ciclo', 'E. Infantil - Segundo ciclo', 'E. Primaria',
                         'Educación Especial', 'ESO', 'Bachillerato', 'Bachillerato a distancia',
                         'CF Grado Básico', 'CF Grado Medio', 'CF Grado Medio a distancia',
                         'Cursos de Especialización Grado Medio', 'Cursos de Especialización Grado Medio a distancia',
                         'CF Grado Superior', 'CF Grado Superior a distancia', 'Cursos de Especialización Grado Superior',
                         'Cursos de Especialización Grado Superior a distancia', 'Otros Programas Formativos']
    filas_objetivo = ['01 ANDALUCÍA']

    # Filtrar solo las filas y columnas deseadas
    df_filtrado = df[df.iloc[:, 0].isin(filas_objetivo)]
    df_final = df_filtrado.set_index(df.columns[0])[columnas_objetivo]

    # Guardar el resultado en un archivo Excel
    output_path = 'resultados/Tabla_2_06.xlsx'
    df_final.to_excel(output_path, index=True)

    messagebox.showinfo("Éxito", f"Tabla 2.06 generada y guardada en {output_path}.")
