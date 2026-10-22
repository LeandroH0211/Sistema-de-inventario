# Sistema de Inventario y Ventas

Aplicación web para gestionar el inventario de productos y registrar ventas,
desarrollada en equipo con Python, Flask y SQLAlchemy.

## Funcionalidades
- [Registrar, editar y eliminar productos]
- [Control de stock]
- [Registro de ventas y su historial]
- [Otras funciones que tenga el sistema]

## Tecnologías
- Python 3
- Flask
- SQLAlchemy
- [SQLite]
- [HTML/CSS/Jinja2]

## Estructura del proyecto
```
app/            # Código de la aplicación (rutas, modelos, plantillas)
run.py          # Punto de entrada para ejecutar la app
seed.py         # Carga datos de ejemplo en la base de datos
check_db.py     # Verifica el estado de la base de datos
requirements.txt
```

## Instalación y uso
1. Clona el repositorio:
   `git clone https://github.com/LeandroH0211/Sistema-de-inventario.git`
2. Crea y activa el entorno virtual:
   `python -m venv .venv`
3. Instala las dependencias (incluye Flask y SQLAlchemy):
   `pip install -r requirements.txt`
4. Crea la base de datos:
   `python -c "from app import create_app; app = create_app()"`
5. (Opcional) Carga datos de prueba:
   `python seed.py`
6. Ejecuta la app:
   `python run.py`
7. Abre en el navegador: `http://localhost:5000`
