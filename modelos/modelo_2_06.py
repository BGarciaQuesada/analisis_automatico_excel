import pandas as pd
import re
import os
import tkinter as tk
from tkinter import messagebox

# [!!!] RECUPERACIÓN DE DATOS EXITOSA, FALTA PLASMARLO CON FORMATO Y LIMPIAR

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
        # Cargar el Excel CON ENCABEZADOS desde la fila 7
        df = pd.read_excel('datos/regimen_general.xls', header=6)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo 'regimen_general.xls':\n{e}")
        return

    # Limpieza de títulos de columnas
    df.columns = [limpiar_titulo(col) if isinstance(col, str) else col for col in df.columns]

    # Limpieza de títulos de la primera columna
    df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: limpiar_titulo(x.strip()) if isinstance(x, str) else x)

    # [!!!] Tiene que haber a la fuerza una mejor forma de hacer esto. Revisar cuando tenga claridad

    # Encontrar índices de las secciones
    todos_los_centros_index = df[df.iloc[:, 0] == 'TODOS LOS CENTROS'].index
    centros_publicos_index = df[df.iloc[:, 0] == 'CENTROS PÚBLICOS'].index

    if todos_los_centros_index.empty or centros_publicos_index.empty:
        messagebox.showerror("Error", "No se encontraron las secciones necesarias.")
        return

    # Filtrar la sección desde "TODOS LOS CENTROS" hasta "CENTROS PÚBLICOS"
    df_seccion = df.iloc[todos_los_centros_index[0]:centros_publicos_index[0]]

    # Encontrar índices dentro de la sección filtrada
    ambos_sexos_index = df_seccion[df_seccion.iloc[:, 0] == 'AMBOS SEXOS'].index
    hombres_index = df_seccion[df_seccion.iloc[:, 0] == 'Hombres'].index
    mujeres_index = df_seccion[df_seccion.iloc[:, 0] == 'Mujeres'].index

    if ambos_sexos_index.empty or hombres_index.empty or mujeres_index.empty:
        messagebox.showerror("Error", "No se encontraron las subsecciones necesarias.")
        return

    # Extraer filas de "01 ANDALUCÍA" en cada sección
    df_final = pd.DataFrame()  # DataFrame para almacenar los resultados

    # Desde "AMBOS SEXOS" hasta "Hombres"
    df_subseccion = df_seccion.iloc[ambos_sexos_index[0]:hombres_index[0]]
    df_final = pd.concat([df_final, df_subseccion[df_subseccion.iloc[:, 0] == '01 ANDALUCÍA']])

    # Desde "Hombres" hasta "Mujeres"
    df_subseccion = df_seccion.iloc[hombres_index[0]:mujeres_index[0]]
    df_final = pd.concat([df_final, df_subseccion[df_subseccion.iloc[:, 0] == '01 ANDALUCÍA']])

    # Desde "Mujeres" hasta el final de la sección
    df_subseccion = df_seccion.iloc[mujeres_index[0]:]
    df_final = pd.concat([df_final, df_subseccion[df_subseccion.iloc[:, 0] == '01 ANDALUCÍA']])

    # Guardar el resultado en un archivo Excel
    output_path = 'resultados/Tabla_2_06.xlsx'
    df_final.to_excel(output_path, index=True)

    messagebox.showinfo("Éxito", f"Tabla 2.06 generada y guardada en {output_path}.")

# [!!!] En un futuro se pretende transformar esto en plantilla
#
# Esta clase se convierte en plantilla y le tengo que pasar: 
# · De qué archivo leer (línea 21: "datos/regimen_general.xls") y su error subsecuente (línea 23)
# · columnas_objetivo (linea 33, array)
# · filas_objetivo (linea 39, array)
# · Nombre del archivo resultado (línea 46, 'resultados/Tabla_2_06.xlsx') y éxito (línea 49)
#
# Como el encabezado es igual en todas, la Limpieza de títulos de columnas se puede mantener