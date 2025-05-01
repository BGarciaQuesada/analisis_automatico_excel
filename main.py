import tkinter as tk
from tkinter import messagebox
import comprobacion_datos
import tabla_predeterminada
import tabla_personalizada
import tutorial

def main():
    # Creación de root (ventana)
    root = tk.Tk()
    root.title("Gestor de Tablas MFYP")
    root.minsize(400, 300)  # Establecer un tamaño mínimo para la ventana

    # Métodos a ser utilizados por los botones
    def on_comprobacion_datos():
        comprobacion_datos.comprobar_datos(root)

    def on_tabla_predeterminada():
        tabla_predeterminada.mostrar_menu_predeterminadas(root)

    def on_tabla_personalizada():
        tabla_personalizada.mostrar_menu_personalizadas(root)

    def on_tutorial():
        tutorial.mostrar_tutorial(root)

    # --- INTERFAZ GRÁFICA (WIP) ---
    tk.Button(root, text="Comprobación de Datos", command=on_comprobacion_datos, width=20, height=2).pack(pady=5)
    tk.Button(root, text="Tabla Predeterminada", command=on_tabla_predeterminada, width=20, height=2).pack(pady=5)
    tk.Button(root, text="Tabla Personalizada", command=on_tabla_personalizada, width=20, height=2).pack(pady=5)
    tk.Button(root, text="Tutorial", command=on_tutorial, width=20, height=2).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
