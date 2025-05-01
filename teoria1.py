import pandas as pd

# Cargar Excel, permitiendo encabezados mezclados
df = pd.read_excel("datos/tabla_regimen_general.xls", header=None)

# Paso 1: Buscar la fila que contiene los encabezados reales (donde está "TOTAL", "Infantil", etc.)
# Supongamos que es la fila que contiene "TOTAL"
header_row_index = df[df.apply(lambda row: row.astype(str).str.contains("TOTAL").any(), axis=1)].index[0]

# Obtener encabezados
columnas = df.iloc[header_row_index]
df.columns = columnas

# Paso 2: Recortar el dataframe desde la siguiente fila
df = df.iloc[header_row_index + 1:].reset_index(drop=True)

# Paso 3: Filtrar por territorio
territorios = ['00 TOTAL', '00 ANDALUCÍA']
df_filtrado = df[df[columnas[0]].isin(territorios)]

# Paso 4: Limpiar columnas y transformar a formato largo
df_limpio = df_filtrado.melt(id_vars=[columnas[0]], var_name='Curso', value_name='Alumnos')
df_limpio = df_limpio.rename(columns={columnas[0]: 'Territorio'})

# Paso 5: Eliminar NaNs y convertir a números
df_limpio = df_limpio.dropna()
df_limpio['Alumnos'] = pd.to_numeric(df_limpio['Alumnos'], errors='coerce')

print(df_limpio)