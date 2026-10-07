import math
import re

from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models import Producto

producto_bp = Blueprint('productos', __name__, url_prefix="/productos")

CATEGORIAS_VALIDAS = ["Electrónica", "Muebles"]
PATRON_NOMBRE = re.compile(r"^[^\W\d_]+(?: [^\W\d_]+)*$")
MAX_PRECIO = 100_000_000
MAX_STOCK = 1_000_000


def _leer_formulario():
    errores = []

    nombre = " ".join(request.form.get("nombre", "").split())
    if not nombre:
        errores.append("El nombre es obligatorio.")
    elif len(nombre) < 2 or len(nombre) > 100:
        errores.append("El nombre debe tener entre 2 y 100 caracteres.")
    elif not PATRON_NOMBRE.match(nombre):
        errores.append("El nombre solo puede contener letras y espacios.")

    descripcion = request.form.get("descripcion", "").strip()
    if not descripcion:
        errores.append("La descripción es obligatoria.")
    elif len(descripcion) > 255:
        errores.append("La descripción no puede superar los 255 caracteres.")

    categoria = request.form.get("categoria", "").strip()
    if categoria not in CATEGORIAS_VALIDAS:
        errores.append("Selecciona una categoría válida.")

    precio = None
    try:
        precio = float(request.form.get("precio", ""))
        if not math.isfinite(precio):
            raise ValueError
    except ValueError:
        errores.append("El precio debe ser un número válido.")
    else:
        if precio <= 0:
            errores.append("El precio debe ser mayor que 0.")
        elif precio > MAX_PRECIO:
            errores.append("El precio es demasiado alto.")

    stock = None
    try:
        stock = int(request.form.get("stock", ""))
    except ValueError:
        errores.append("El stock debe ser un número entero.")
    else:
        if stock <= 0:
            errores.append("El stock no puede ser negativo.")
        elif stock > MAX_STOCK:
            errores.append("El stock es demasiado alto.")

    stock_minimo = None
    try:
        stock_minimo = int(request.form.get("stock_minimo", ""))
    except ValueError:
        errores.append("El stock mínimo debe ser un número entero.")
    else:
        if stock_minimo < 0:
            errores.append("El stock mínimo no puede ser negativo.")
        elif stock_minimo > MAX_STOCK:
            errores.append("El stock mínimo es demasiado alto.")

    if errores:
        raise ValueError(" | ".join(errores))

    return {
        "nombre": nombre,
        "descripcion": descripcion,
        "categoria": categoria,
        "precio": precio,
        "stock": stock,
        "stock_minimo": stock_minimo,
    }


def _redirigir_a_lista(producto):
    if producto.stock < producto.stock_minimo:
        return redirect(url_for("productos.lista", advertencia=producto.id_producto))
    return redirect(url_for("productos.lista"))


@producto_bp.route("/")
def lista():
    error = None
    advertencia = None
    productos = []

    try:
        productos = Producto.query.all()

        id_advertencia = request.args.get("advertencia", type=int)
        if id_advertencia:
            producto = db.session.get(Producto, id_advertencia)
            if producto and producto.stock < producto.stock_minimo:
                advertencia = (
                    f"El producto «{producto.nombre}» se guardó, pero su stock "
                    f"({producto.stock}) es menor al stock mínimo ({producto.stock_minimo})."
                )
    except SQLAlchemyError as e:
        print(f"Error al listar productos: {e}")
        error = "No se pudo cargar la lista de productos."

    return render_template(
        "productos/lista.html",
        productos=productos,
        error=error,
        advertencia=advertencia,
    )


@producto_bp.route("/nuevo_p", methods=["GET", "POST"])
def nuevo():
    error = None

    if request.method == "POST":
        try:
            datos = _leer_formulario()
            producto = Producto(**datos)
            db.session.add(producto)
            db.session.commit()
            return _redirigir_a_lista(producto)

        except ValueError as e:
            error = str(e)

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al crear producto: {e}")
            error = "Error al guardar el producto en la base de datos."

        except Exception as e:
            db.session.rollback()
            print(f"Error inesperado al crear producto: {e}")
            error = "Ocurrió un error inesperado."

    return render_template("productos/nuevo_p.html", error=error)


@producto_bp.route("/eliminar/<int:id_producto>")
def eliminar(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    try:
        db.session.delete(producto)
        db.session.commit()

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error al eliminar producto {id_producto}: {e}")
        productos = Producto.query.all()
        return render_template(
            "productos/lista.html",
            productos=productos,
            error="No se pudo eliminar el producto (puede tener registros asociados).",
            advertencia=None,
        )

    return redirect(url_for("productos.lista"))


@producto_bp.route("/editar/<int:id_producto>", methods=["GET", "POST"])
def editar(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    error = None

    if request.method == "POST":
        try:
            datos = _leer_formulario()
            for campo, valor in datos.items():
                setattr(producto, campo, valor)

            db.session.commit()
            return _redirigir_a_lista(producto)

        except ValueError as e:
            db.session.rollback()
            error = str(e)

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Error al editar producto {id_producto}: {e}")
            error = "Error al actualizar el producto en la base de datos."

        except Exception as e:
            db.session.rollback()
            print(f"Error inesperado al editar producto {id_producto}: {e}")
            error = "Ocurrió un error inesperado."

    return render_template("productos/editar.html", producto=producto, error=error)