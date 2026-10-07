from flask import Blueprint, render_template
from sqlalchemy import func
from app.models import Producto, Cliente, Venta
from app.database import db              

home_bp = Blueprint("main", __name__)

@home_bp.route("/")
def index():
    total_productos = Producto.query.count()
    total_clientes = Cliente.query.count()
    total_ventas = Venta.query.count()

    return render_template(
        "index.html",
        total_productos=total_productos,
        total_clientes=total_clientes,
        total_ventas=total_ventas,
    )