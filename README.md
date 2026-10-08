comandos a realizar:
python -m venv .venv
pip install -r requirements.txt, esto instala flask y sqlalchemy
python -c "from app import create_app; app = create_app()", esto crea la database
python seed.py, esto agrega datos falsos a la base de datos
python run.py para correr la app
