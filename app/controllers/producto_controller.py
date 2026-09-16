from flask import Blueprint, render_template

producto_bp = Blueprint('productos', __name__, url_prefix="/productos")

@producto_bp.route("/")
def lista():
    return render_template("productos/lista.html", productos=[])