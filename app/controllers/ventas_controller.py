from flask import Blueprint, render_template

ventas = Blueprint('ventas', __name__)

@ventas.route('/ventas/nueva')
def nueva_venta():
    return render_template('ventas/nueva_venta.html')

@ventas.route('/ventas/historial')
def historial_ventas():
    return render_template('ventas/historial_ventas.html')