import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont  # Para las imagenes
import os
import webbrowser  # Funcionalidad del enlace
from functools import partial  # Para el debounce del redimensionamiento

class TutorialApp:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        
        # Crear ventana de tutorial
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Tutorial - Gestor de Tablas MEFPYD")
        
        # Configuración de tamaño (Orden cambiado, ahora funciona)
        self.ventana.geometry("1000x700") # Tamaño inicial
        self.ventana.minsize(800, 600) # Tamaño mínimo
        
        # Configuración de pasos del tutorial
        self.pasos = [
            {
                "titulo": "Bienvenido al Gestor de Tablas MEFPYD",
                "imagen": "imagenes/bienvenida.png",
                "texto": "La función de este programa es agilizar el proceso de creación de tablas para el informe elaborado por el Consejo Escolar Andalucía en relación a las cifras de educación."
            },
            {
                "titulo": "Descarga de los archivos",
                "imagen": "imagenes/paso1.png",
                "texto": "Acceda al portal de datos abiertos del MEFPYD (localizado abajo) y seleccione la estadística pertinente",
                "enlace": "https://www.educacionfpydeportes.gob.es/servicios-al-ciudadano/estadisticas.html"
            },
            {
                "titulo": "Descarga de los archivos",
                "imagen": "imagenes/paso2.png",
                "texto": "Se le presentarán las distintas secciones.\nAl nutrirse la mayoría de Estadísticas del MEFD → Enseñanzas no universitarias, seguiremos esta ruta en el tutorial."
            },
            {
                "titulo": "Descarga de los archivos",
                "imagen": "imagenes/paso3.png",
                "texto": "Elija el año del que quiera recoger los datos.\n\nRecuerde que siempre puede comprobar el año de cada archivo en 'Comprobación de Datos' desde el menú principal."
            },
            {
                "titulo": "Descarga de los archivos",
                "imagen": "imagenes/paso4.png",
                "texto": "Haga click en el símbolo a la derecha del nombre de la tabla [Eb] para acceder a las descargas."
            },
            {
                "titulo": "Descarga de los archivos",
                "imagen": "imagenes/paso5.png",
                "texto": "Descargue las tablas necesarias:\n\n- Haga clic en la flecha a la izquierda de cada una para descarga directa o, alternativamente, en el nombre para realizar una consulta manual"
            }
        ]
        
        self.paso_actual = 0
        
        # Configurar interfaz
        self.setup_ui()
        self.mostrar_paso()
    
    # --- INTERFAZ GRÁFICA ---

    # Método para configurar todos los elementos
    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.ventana)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título del paso
        self.titulo = ttk.Label(
            main_frame, 
            font=('Arial', 14, 'bold'),
            justify=tk.CENTER
        )
        self.titulo.pack(pady=10)
        
        # Contenedor de imagen
        img_frame = ttk.Frame(main_frame)
        img_frame.pack(fill=tk.BOTH, expand=True)
        
        # Canvas para la imagen
        self.canvas = tk.Canvas(img_frame, bg='#f0f0f0', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Vincular redimensionamiento del canvas (debounce para mejor rendimiento)
        self.canvas.bind("<Configure>", lambda e: self.ventana.after(100, partial(self.redibujar_imagen_actual)))
        
        # Frame para el texto descriptivo
        texto_frame = ttk.Frame(main_frame)
        texto_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.texto = tk.Text(
            texto_frame, 
            wrap=tk.WORD, 
            font=('Arial', 11),
            height=5,
            padx=10,
            pady=10,
            bg='#f9f9f9',
            relief=tk.FLAT
        )
        self.texto.pack(fill=tk.BOTH, expand=True)
        
        # Frame para botones de navegación
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        # Botones de navegación
        self.btn_anterior = ttk.Button(
            btn_frame, 
            text="← Anterior",
            command=self.anterior_paso,
            state=tk.DISABLED
        )
        self.btn_anterior.pack(side=tk.LEFT, padx=5)
        
        self.btn_siguiente = ttk.Button(
            btn_frame, 
            text="Siguiente →",
            command=self.siguiente_paso
        )
        self.btn_siguiente.pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Regresar",
            command=self.cerrar_tutorial
        ).pack(side=tk.RIGHT, padx=20)
        
        # Contador de pasos
        self.contador = ttk.Label(
            btn_frame,
            font=('Arial', 10, 'bold'),
            foreground='#555555'
        )
        self.contador.pack(side=tk.BOTTOM, pady=5)
    
    # Manejar el redibujado durante redimensionamiento
    def redibujar_imagen_actual(self, event=None):
        if hasattr(self, 'paso_actual') and 0 <= self.paso_actual < len(self.pasos):
            paso = self.pasos[self.paso_actual]
            self.mostrar_imagen(paso["imagen"], event)

    # Método para mostrar el paso actual
    def mostrar_paso(self):
        self.ventana.update_idletasks()  # Actualiza geometría
        
        paso = self.pasos[self.paso_actual]
        
        # Actualizar título
        self.titulo.config(text=paso["titulo"])
        
        # Actualizar texto
        self.texto.config(state=tk.NORMAL)
        self.texto.delete(1.0, tk.END)
        self.texto.insert(tk.END, paso["texto"])
        
        # Añadir enlace si existe
        if "enlace" in paso:
            self.texto.insert(tk.END, "\n\n[Enlace oficial]", "enlace")
            self.texto.tag_config("enlace", foreground="blue", underline=1) # Formato azul y subrayado
            self.texto.tag_bind("enlace", "<Button-1>", 
                              lambda e: webbrowser.open(paso["enlace"])) # Hacer clic abre enlace
            self.texto.tag_bind("enlace", "<Enter>", 
                              lambda e: self.texto.config(cursor="hand2")) # Pasar el culsor cambia a dedo apuntando
            self.texto.tag_bind("enlace", "<Leave>", 
                              lambda e: self.texto.config(cursor="")) # Apartar el cursor lo resetea a como estaba
        
        self.texto.config(state=tk.DISABLED)
        
        # Cargar y mostrar imagen
        self.mostrar_imagen(paso["imagen"])
        
        # Actualizar contador
        self.contador.config(text=f"Paso {self.paso_actual + 1}/{len(self.pasos)}")
        
        # Actualizar estado de los botones
        self.btn_anterior.config(state=tk.NORMAL if self.paso_actual > 0 else tk.DISABLED)
        self.btn_siguiente.config(
            text="Finalizar" if self.paso_actual == len(self.pasos) - 1 else "Siguiente →"
        )
    
    # Renderizar imagen del paso actual REDIMENSIONADA
    def mostrar_imagen(self, ruta_imagen, event=None):
        try:
            # Limpiar canvas
            self.canvas.delete("all")
            
            # Obtener dimensiones del canvas (del evento o del widget)
            if event:
                canvas_width = event.width
                canvas_height = event.height
            else:
                canvas_width = self.canvas.winfo_width()
                canvas_height = self.canvas.winfo_height()
            
            # Valores por defecto si el canvas es muy pequeño
            if canvas_width < 100 or canvas_height < 100:
                canvas_width = 800
                canvas_height = 500
            
            # Margen para no pegar la imagen a los bordes
            margin = 20
            max_width = canvas_width - margin * 2
            max_height = canvas_height - margin * 2
            
            # Cargar imagen (texto en caso de error)
            if os.path.exists(ruta_imagen):
                img = Image.open(ruta_imagen)
            else:
                img = Image.new('RGB', (800, 500), color='#f0f0f0')
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("arial.ttf", 20)
                except:
                    font = ImageFont.load_default()
                draw.text((50, 50), f"Imagen no encontrada:\n{ruta_imagen}", 
                         fill="red", font=font)
            
            # Redimensionar manteniendo relación de aspecto
            img_ratio = img.width / img.height
            canvas_ratio = max_width / max_height
            
            if img_ratio > canvas_ratio:
                new_width = max_width
                new_height = int(max_width / img_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * img_ratio)
            
            img_resized = img.resize((new_width, new_height), Image.LANCZOS)
            self.img_tk = ImageTk.PhotoImage(img_resized)  # Guardar como atributo
            
            # Calcular posición centrada
            x_pos = (canvas_width - new_width) // 2
            y_pos = (canvas_height - new_height) // 2
            
            # Mostrar imagen en canvas
            self.canvas.create_image(
                x_pos + margin, 
                y_pos + margin, 
                anchor=tk.NW, 
                image=self.img_tk
            )

        # Mensaje de error si no se encontrase la imagen  
        except Exception as e:
            print(f"Error cargando imagen: {e}")
            self.canvas.create_text(
                canvas_width//2, 
                canvas_height//2, 
                text=f"Error cargando imagen:\n{e}",
                fill="red",
                font=('Arial', 12),
                anchor=tk.CENTER
            )
    
    # Método para avanzar (se bloquea si está en el último paso)
    def siguiente_paso(self):
        if self.paso_actual < len(self.pasos) - 1:
            self.paso_actual += 1
            self.mostrar_paso()
        else:
            self.cerrar_tutorial()

    # Método para retroceder (se bloquea si está en el primero paso)
    def anterior_paso(self):
        if self.paso_actual > 0:
            self.paso_actual -= 1
            self.mostrar_paso()
    
    # Cerrar ventana
    def cerrar_tutorial(self):
        self.ventana.destroy()
        self.root.deiconify()

def mostrar_tutorial(root):
    TutorialApp(root)