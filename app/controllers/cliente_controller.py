import secrets
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models import Cliente

cliente_bp = Blueprint('clientes', __name__, url_prefix="/clientes")


@cliente_bp.route("/")
def lista():
    busqueda = request.args.get("q", "").strip()

    query = Cliente.query
    if busqueda:
        query = query.filter(Cliente.nombre.ilike(f"%{busqueda}%"))

    clientes = query.all()

    return render_template(
        "clientes/lista.html",
        clientes=clientes,
        busqueda=busqueda,
    )


@cliente_bp.route("/nuevo_c", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        id_cliente = secrets.randbelow(900000) + 100000
        while db.session.get(Cliente, id_cliente) is not None:
            id_cliente = secrets.randbelow(900000) + 100000

        cliente = Cliente(
            id_cliente=id_cliente,
            nombre=request.form["nombre"],
            direccion=request.form["direccion"],
            telefono=request.form["telefono"],
            email=request.form["email"]
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for("clientes.lista"))

    return render_template("clientes/nuevo_c.html")


@cliente_bp.route("/eliminar/<int:id_cliente>", methods=["POST"])
def eliminar(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    try:
        
        for venta in cliente.ventas:
            for detalle in venta.detalles:
                detalle.producto.stock += detalle.cantidad

        db.session.delete(cliente)   
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al eliminar cliente: {e}")
    return redirect(url_for("clientes.lista"))


@cliente_bp.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
def editar(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)

    if request.method == "POST":
        cliente.nombre = request.form["nombre"]
        cliente.direccion = request.form["direccion"]
        cliente.telefono = request.form["telefono"]
        cliente.email = request.form["email"]

        db.session.commit()
        return redirect(url_for("clientes.lista"))

    return render_template("clientes/editar.html", cliente=cliente)