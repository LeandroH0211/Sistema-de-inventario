from flask import Blueprint, render_template, request, redirect, url_for
from app.database import db
from app.models import Producto

producto_bp = Blueprint('productos', __name__, url_prefix="/productos")

@producto_bp.route("/")
def lista():
    productos = Producto.query.all()
    return render_template("productos/lista.html", productos=productos)

@producto_bp.route("/nuevo_p", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        producto = Producto(
            descripcion=request.form["descripcion"],
            categoria=request.form["categoria"],
            precio=request.form["precio"],
            stock=request.form["stock"],
            stock_minimo=request.form["stock_minimo"]
        )
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for("productos.lista"))

    return render_template("productos/nuevo_p.html")

@producto_bp.route("/eliminar/<int:id_producto>")
def eliminar(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("productos.lista"))

@producto_bp.route("/editar/<int:id_producto>", methods=["GET", "POST"])
def editar(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    if request.method == "POST":
        producto.descripcion = request.form["descripcion"]
        producto.categoria = request.form["categoria"]
        producto.precio = request.form["precio"]
        producto.stock = request.form["stock"]
        producto.stock_minimo = request.form["stock_minimo"]

        db.session.commit()
        return redirect(url_for("productos.lista"))

    return render_template("productos/editar.html", producto=producto)