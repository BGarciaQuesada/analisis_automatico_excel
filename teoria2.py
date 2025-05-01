import pandas as pd

# Cargar el archivo Excel con la hoja correspondiente
df = pd.read_excel('nombre_del_archivo.xlsx', sheet_name='Hoja1', header=6)  # Header en fila 7 (índice 6)

# Filtramos por filas (índices deseados)
filas_deseadas = ['TOTAL', 'E. Primaria', 'ESO']

# Filtramos por columnas deseadas (que corresponden a las provincias/comunidades)
columnas_deseadas = ['TOTAL', '01 ANDALUCIA', 'Cádiz']

# Este DataFrame tiene muchas columnas con nombres tipo 'TOTAL.1', 'TOTAL.2', etc. Lo más probable es que tengas que revisar cómo pandas interpreta los nombres reales de columnas al cargarlo.
# Para ayudarte a entender qué columnas están disponibles, podrías hacer:
print(df.columns)

# Una vez indentificados los nombres reales de las columnas (por ejemplo 'TOTAL', 'TOTAL.1', etc.), puedes hacer:
df_filtrado = df[df.iloc[:, 0].isin(filas_deseadas)]  # Seleccionamos filas por la primera columna (nombres de indicadores)

# Asumimos que las columnas relevantes están mapeadas correctamente
df_final = df_filtrado[['TOTAL', '01 ANDALUCÍA', 'Cádiz']]

# Si deseas, puedes cambiar el índice:
df_final.set_index(df_final.columns[0], inplace=True)

print(df_final)
