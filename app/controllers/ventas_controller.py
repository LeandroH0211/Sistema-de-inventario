from datetime import date
from decimal import Decimal, InvalidOperation

from flask import Blueprint, render_template, request, redirect, url_for

from app.database import db
from app.models import Cliente, Producto, Venta, DetalleVenta

ventas = Blueprint('ventas', __name__)

@ventas.route('/ventas/nueva', methods=['GET', 'POST'])
def nueva_venta():
    if request.method == 'POST':
        id_cliente = request.form.get('id_cliente', type=int)
        fecha = request.form.get('fecha')
        estado = request.form.get('estado', 'Pendiente')
        tipo_descuento = request.form.get('tipo_descuento', 'porcentual')

        try:
            fecha_venta = date.fromisoformat(fecha)
            valor_descuento = Decimal(request.form.get('descuento', '1'))
        except (TypeError, ValueError, InvalidOperation):
            return 'Los datos de la venta no son válidos.', 400

        cliente = db.session.get(Cliente, id_cliente)
        if cliente is None or valor_descuento < 1:
            return 'El cliente o el descuento no son válidos.', 400

        ids_producto = request.form.getlist('id_producto')
        cantidades = request.form.getlist('cantidad')
        lineas = []
        cantidades_por_producto = {}

        try:
            for id_producto, cantidad in zip(ids_producto, cantidades):
                if not id_producto:
                    continue

                id_producto = int(id_producto)
                cantidad = int(cantidad)
                if cantidad < 1:
                    return 'La cantidad debe ser mayor o igual a 1.', 400

                cantidades_por_producto[id_producto] = (
                    cantidades_por_producto.get(id_producto, 0) + cantidad
                )
                lineas.append((id_producto, cantidad))
        except ValueError:
            return 'Los productos o cantidades no son válidos.', 400

        if not lineas:
            return 'Debe agregar al menos un producto.', 400

        productos = {
            producto.id_producto: producto
            for producto in Producto.query.filter(
                Producto.id_producto.in_(cantidades_por_producto)
            ).with_for_update()
        }

        subtotal = Decimal('0')
        for id_producto, cantidad_total in cantidades_por_producto.items():
            producto = productos.get(id_producto)
            if producto is None or cantidad_total > producto.stock:
                return 'La cantidad solicitada supera el stock disponible.', 400
            subtotal += producto.precio * cantidad_total

        descuento = (
            subtotal * valor_descuento / Decimal('100')
            if tipo_descuento == 'porcentual'
            else valor_descuento
        )
        total = max(Decimal('0'), subtotal - descuento)

        venta = Venta(
            id_cliente=id_cliente,
            fecha=fecha_venta,
            estado=estado,
            total=total
        )
        db.session.add(venta)

        for id_producto, cantidad in lineas:
            producto = productos[id_producto]
            subtotal_linea = producto.precio * cantidad
            db.session.add(DetalleVenta(
                venta=venta,
                id_producto=id_producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal_linea
            ))
            producto.stock -= cantidad

        db.session.commit()
        return redirect(url_for('ventas.historial_ventas'))

    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.order_by(Producto.nombre).all()
    return render_template(
        'ventas/nueva_venta.html',
        clientes=clientes,
        productos=productos
    )

@ventas.route('/ventas/historial')
def historial_ventas():
    ventas_registradas = Venta.query.order_by(Venta.fecha.desc(), Venta.id_venta.desc()).all()
    return render_template(
        'ventas/historial_ventas.html',
        ventas=ventas_registradas
    )