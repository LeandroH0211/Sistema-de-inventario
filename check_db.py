from app import create_app
from app.models import Cliente, Producto, Venta, DetalleVenta

app = create_app()

with app.app_context():
    print("=== CLIENTES ===")
    for c in Cliente.query.all():
        print(f"{c.id_cliente} | {c.nombre} | {c.email} | {c.telefono}")

    print("\n=== PRODUCTOS ===")
    for p in Producto.query.all():
        print(f"{p.id_producto} | {p.descripcion} | {p.categoria} | ${p.precio} | stock: {p.stock}")

    print("\n=== VENTAS ===")
    for v in Venta.query.all():
        print(f"{v.id_venta} | Cliente: {v.cliente.nombre} | {v.fecha} | {v.estado} | ${v.total}")

    print("\n=== DETALLE_VENTA ===")
    for d in DetalleVenta.query.all():
        print(f"{d.id_detalle} | Venta {d.id_venta} | {d.producto.descripcion} | cant: {d.cantidad} | ${d.subtotal}")