import tkinter as tk
from tkinter import ttk, messagebox
import comprobacion_datos
import tabla_predeterminada
import tabla_personalizada
import tutorial
from PIL import Image, ImageTk  # Para imagen del logo

def main():
    # Creación de root (ventana) con nuevo estilo
    root = tk.Tk()
    root.title("Gestor de Tablas MEFPYD")
    root.minsize(800, 600)  # Tamaño mínimo más grande
    
    # Frame principal
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    # Cabecera (Imagen + Título)
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(pady=(0, 20))
    
    # Cargar imagen
    try:
        img = Image.open("imagenes/logo.png")
        img = img.resize((128, 128), Image.Resampling.LANCZOS)  # Redimensionar
        logo_img = ImageTk.PhotoImage(img)
        
        logo_label = ttk.Label(header_frame, image=logo_img)
        logo_label.image = logo_img  # Mantener referencia
        logo_label.pack()
    except FileNotFoundError:
        # No tiene que salir por ningún lado, no es vital, hago print y ya
        print("Advertencia: No se encontró el archivo de logo.png")
    
    # Título
    title_label = ttk.Label(header_frame, 
                          text="Gestor de Tablas MEFPYD", 
                          font=('Arial', 20, 'bold'))
    title_label.pack(pady=(10, 20))
    
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

    # Botones
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