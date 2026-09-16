from app.database import db

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))

    ventas = db.relationship('Venta', backref='cliente', lazy=True)


