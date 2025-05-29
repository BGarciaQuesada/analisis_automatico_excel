import pandas as pd
import re
import os
import tkinter as tk
from tkinter import messagebox

class ModeloPlantilla:
    def __init__(self, archivos_entrada, archivo_salida, secciones, subsecciones, filas_objetivo):
        self.archivos_entrada = archivos_entrada
        self.archivo_salida = archivo_salida
        self.secciones = secciones
        self.subsecciones = subsecciones
        self.filas_objetivo = filas_objetivo

    def limpiar_texto(self, texto):
        if not isinstance(texto, str):
            return texto
        texto = re.sub(r"\s*[\(\[].*?[\)\]]", "", texto) # Elimina texto entre paréntesis/corchetes
        texto = re.sub(r"\s*\*.*$", "", texto) # Elimina texto después de asteriscos
        return texto.strip() # Elimina espacios en blanco al inicio/final

    def ejecutar_modelo(self, root):
        try:
            # Verificar directorio de datos
            if not os.path.exists('datos'):
                os.makedirs('datos')
                raise FileNotFoundError("Directorio 'datos' creado. Coloque los archivos allí.")

            resultados = []

            for archivo in self.archivos_entrada:
                # Leer archivo
                df = pd.read_excel(archivo, header=6)

                # Limpiar columnas
                df.columns = [self.limpiar_texto(col) if isinstance(col, str) else col for col in df.columns]
                df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: self.limpiar_texto(x) if isinstance(x, str) else x)

                # > Me he dado cuenta de que antes solo marcaba 1 fila después
                # > de la sección en lugar de cogerla entera. Arreglado.

                # Procesar cada sección
                for i, seccion in enumerate(self.secciones):
                    # Encontrar la sección
                    idx_seccion = df.index[df.iloc[:, 0] == seccion].tolist()
                    if not idx_seccion:
                        continue

                    start = idx_seccion[0]

                    # Determinar el fin de la sección
                    if i < len(self.secciones) - 1:
                        # Buscar siguiente sección en la lista
                        next_seccion = self.secciones[i + 1]
                        idx_next = df.index[df.iloc[:, 0] == next_seccion].tolist()
                        end = idx_next[0] if idx_next else len(df)
                    else:
                        # Última sección va hasta el final
                        end = len(df)

                    # Filtrar subsecciones
                    df_seccion = df.iloc[start:end].copy()

                    for sub in self.subsecciones:
                        idx_sub = df_seccion.index[df_seccion.iloc[:, 0] == sub].tolist()
                        if not idx_sub:
                            continue

                        start_sub = idx_sub[0]
                        end_sub = start_sub + 1

                        # Encontrar el final de la subsección
                        while (end_sub < len(df_seccion)) and (df_seccion.iloc[end_sub, 0] not in self.subsecciones):
                            end_sub += 1

                        # Filtrar filas objetivo
                        df_sub = df_seccion.iloc[start_sub:end_sub].copy()
                        df_filas = df_sub[df_sub.iloc[:, 0].isin(self.filas_objetivo)].copy()

                        if not df_filas.empty:
                            # Nuevo DataFrame con las columnas en el orden correcto
                            df_filas = pd.DataFrame({
                                'Sección': seccion,
                                'Subsección': sub,
                                'Fila': df_filas.iloc[:, 0],
                                **{col: df_filas[col] for col in df_filas.columns[1:]}
                            })

                            resultados.append(df_filas)

            if resultados:
                df_final = pd.concat(resultados, ignore_index=True)
                df_final = df_final.loc[:, ~df_final.columns.duplicated()]

                df_final.to_excel(self.archivo_salida, index=False)
                messagebox.showinfo("Éxito", f"Archivo generado:\n{self.archivo_salida}")
            else:
                messagebox.showwarning("Advertencia", "No se encontraron datos con los criterios seleccionados")

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")