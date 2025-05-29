# Gestor de Tablas MEFPYD

Un programa para agilizar la extracción y procesamiento de datos de tablas Excel del Ministerio de Educación, Formación Profesional y Deportes (MEFPYD) para la generación de informes.


## Características

### Comprobación automática de archivos de datos

Leyendo los archivos añadidos por el usuario en el directorio **"datos"**, el programa informará cuáles es capaz de reconocer y a que curso pertenecen.

**Objetivo:** Mostrar al usuario claramente los datos faltantes y evitar el error humano de tomar datos de un curso incorrecto.

### Generación de tablas predeterminadas con configuraciones predefinidas

Se dispone de un csv de modelos que el usuario puede editar para guardar y editar las plantillas predeterminadas del informe.

Dichos modelos deben seguir el siguiente formato:

```bash
nombre_modelo,archivos_entrada,secciones,subsecciones,filas_objetivo
"Modelo 1","['datos/ruta.xls']","['Seccion1', 'Seccion2', ...]","['Subseccion1', 'Subseccion2', ...]","['Fila1','Fila2', ...]"
```

**Objetivo:** Poner a disposición del usuario una fácil plantilla para crear sus propios modelos

### Generación de tablas personalizadas

Se ofrece una selección flexible de:
- Secciones
- Subsecciones
- Filas específicas

**Objetivo:** Ofrecer una alternativa rápida a los modelos predeterminados al usuario.

### Tutorial integrado con guía paso a paso

**Objetivo:** Evitar que el usuario tenga que recurrir a información fuera de la vista gráfica del programa 

### Interfaz gráfica intuitiva basada en Tkinter

**Objetivo:** Hacerlo atractivo y claro visualmente para el usuario.
## Instalación

Clona el repositorio:

```bash
git clone https://github.com/BGarciaQuesada/gestor_tablas_mefpyd.git
cd gestor_tablas_mefpyd
```

Instala las dependencias:
```bash
pip install pandas openpyxl Pillow
```

Inicia la aplicación:
```bash
python main.py
```    
## Estructura del Proyecto

```
📦 gestor-tablas-mefpyd  
├── 📄 main.py                 # Punto de entrada principal  
├── 📄 comprobacion_datos.py   # Módulo de verificación  
├── 📄 tabla_predeterminada.py # Modelos predefinidos  
├── 📄 tabla_personalizada.py  # Modelos personalizados
├── 📄 tutorial.py             # Tutorial interactivo  
├── 📄 plantilla.py            # Procesamiento de datos  
├── 📂 modelos  
│   └── 📄 modelos_config.csv # Configuraciones  
├── 📂 datos                  # Archivos Excel fuente 
├── 📂 resultados             # Archivos generados 
└── 📂 imagenes               # Recursos gráficos
```
