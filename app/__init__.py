from flask import Flask
from app.database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from app.controllers.producto_controller import producto_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.ventas_controller import ventas

    app.register_blueprint(producto_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(ventas)

    with app.app_context():
        from app import models 
        db.create_all()

    return app