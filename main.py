import tkinter as tk
from tkinter import messagebox
import comprobacion_datos
import tabla_predeterminada
import tabla_personalizada
import tutorial

def main():
    root = tk.Tk()
    root.title("Gestor de Tablas MFYP")

    def on_comprobacion_datos():
        comprobacion_datos.comprobar_datos(root)

    def on_tabla_predeterminada():
        tabla_predeterminada.mostrar_menu_predeterminadas(root)

    def on_tabla_personalizada():
        tabla_personalizada.mostrar_menu_personalizadas(root)

    def on_tutorial():
        tutorial.mostrar_tutorial(root)

    tk.Button(root, text="Comprobación de Datos", command=on_comprobacion_datos).pack(pady=5)
    tk.Button(root, text="Tabla Predeterminada", command=on_tabla_predeterminada).pack(pady=5)
    tk.Button(root, text="Tabla Personalizada", command=on_tabla_personalizada).pack(pady=5)
    tk.Button(root, text="Tutorial", command=on_tutorial).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
