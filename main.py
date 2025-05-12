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
    root.minsize(600, 400)  # Tamaño mínimo de la ventana

    # Métodos a ser utilizados por los botones
    def on_comprobacion_datos():
        root.withdraw()  # Ocultar la ventana actual
        comprobacion_datos.comprobar_datos(root)

    def on_tabla_predeterminada():
        root.withdraw()  # Ocultar la ventana actual
        tabla_predeterminada.mostrar_menu_predeterminadas(root)

    def on_tabla_personalizada():
        root.withdraw()  # Ocultar la ventana actual
        tabla_personalizada.mostrar_menu_personalizadas(root)

    def on_tutorial():
        root.withdraw()  # Ocultar la ventana actual
        tutorial.mostrar_tutorial(root)

    # --- INTERFAZ GRÁFICA (WIP) ---
    tk.Button(root, text="Comprobación de Datos", command=on_comprobacion_datos, width=20, height=2).pack(pady=10, padx=20, expand=True, fill=tk.BOTH)
    tk.Button(root, text="Tabla Predeterminada", command=on_tabla_predeterminada, width=20, height=2).pack(pady=10, padx=20, expand=True, fill=tk.BOTH)
    tk.Button(root, text="Tabla Personalizada", command=on_tabla_personalizada, width=20, height=2).pack(pady=10, padx=20, expand=True, fill=tk.BOTH)
    tk.Button(root, text="Tutorial", command=on_tutorial, width=20, height=2).pack(pady=10, padx=20, expand=True, fill=tk.BOTH)

    root.mainloop()

if __name__ == "__main__":
    main()
