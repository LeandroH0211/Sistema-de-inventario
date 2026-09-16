from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.controllers.producto_controller import producto_bp
    from app.controllers.cliente_controller import cliente_bp
    from app.controllers.ventas_controller import ventas

    app.register_blueprint(producto_bp)
    app.register_blueprint(cliente_bp)
    app.register_blueprint(ventas)

    return app