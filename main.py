import tkinter as tk
from tkinter import ttk, messagebox
import comprobacion_datos
import tabla_predeterminada
import tabla_personalizada
import tutorial

def main():
    # Creación de root (ventana) con nuevo estilo
    root = tk.Tk()
    root.title("Gestor de Tablas MFYP")
    root.minsize(800, 600)  # Tamaño mínimo más grande
    
    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Métodos a ser utilizados por los botones
    def on_comprobacion_datos():
        root.withdraw()
        comprobacion_datos.comprobar_datos(root)

    def on_tabla_predeterminada():
        root.withdraw()
        tabla_predeterminada.mostrar_menu_predeterminadas(root)

    def on_tabla_personalizada():
        root.withdraw()
        tabla_personalizada.mostrar_menu_personalizadas(root)

    def on_tutorial():
        root.withdraw()
        tutorial.mostrar_tutorial(root)

    # --- INTERFAZ GRÁFICA ---
    
    btn_style = ttk.Style()
    btn_style.configure('TButton', font=('Arial', 12), padding=10)
    
    ttk.Button(main_frame, text="Comprobación de Datos", 
              command=on_comprobacion_datos, style='TButton').pack(pady=10, fill=tk.X)
    ttk.Button(main_frame, text="Tabla Predeterminada", 
              command=on_tabla_predeterminada, style='TButton').pack(pady=10, fill=tk.X)
    ttk.Button(main_frame, text="Tabla Personalizada", 
              command=on_tabla_personalizada, style='TButton').pack(pady=10, fill=tk.X)
    ttk.Button(main_frame, text="Tutorial", 
              command=on_tutorial, style='TButton').pack(pady=10, fill=tk.X)

    root.mainloop()

if __name__ == "__main__":
    main()