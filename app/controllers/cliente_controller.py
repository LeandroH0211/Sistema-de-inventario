from flask import Blueprint, render_template

cliente_bp = Blueprint('clientes', __name__, url_prefix="/clientes")

@cliente_bp.route("/")
def lista():
    return render_template("clientes/lista.html", clientes=[])