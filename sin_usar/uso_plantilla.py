import tkinter as tk

from plantilla_test import ModeloPlantilla

# EJEMPLO DE USO DE LA PLANTILLA, NO INCLUIDO EN PRODUCTO FINAL!!!
# Se puede encontrar empleado en tabla_predeterminada

# Crear una instancia de la clase ModeloPlantilla con los parámetros necesarios
modelo = ModeloPlantilla(
    archivo_entrada='datos/regimen_general.xls',
    archivo_salida='resultados/Tabla_2_06.xlsx',
    secciones=['TODOS LOS CENTROS', 'CENTROS PÚBLICOS'],
    subsecciones=['AMBOS SEXOS', 'Hombres', 'Mujeres'],
    filas_objetivo=['01 ANDALUCÍA']
)

# Crear una ventana raíz de tkinter (necesaria para los messagebox)
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal

# Ejecutar el modelo
modelo.ejecutar_modelo(root)
