"""
Datos falsos para Sistema-de-inventario.

Uso (desde la carpeta raíz, junto a run.py, con el venv activado):
    python seed.py            -> agrega los datos de prueba
    python seed.py --reset    -> borra todo y luego agrega los datos
"""
import random
import sys
from datetime import date, timedelta
from decimal import Decimal

# Ajusta esta importación a como crees tu app (mira run.py).
from app import create_app
from app.database import db
from app.models import Cliente, Producto, Venta, DetalleVenta

random.seed(42)  # resultados repetibles; quita esta línea si quieres datos distintos cada vez

NOMBRES = [
    "Carlos Ramírez", "Laura Gómez", "Andrés Torres", "María Fernanda Ruiz",
    "Juan Pablo Herrera", "Valentina Castro", "Sebastián Moreno", "Daniela Ortiz",
    "Camilo Vargas", "Natalia Mejía", "Felipe Rojas", "Isabela Cardona",
    "Santiago Londoño", "Paula Andrea Silva", "Mateo Salazar", "Juliana Pineda",
    "Diego Arango", "Camila Restrepo", "Nicolás Ospina", "Sofía Quintero",
]
CALLES = ["Calle 5", "Carrera 15", "Avenida 3N", "Calle 34", "Carrera 100", "Transversal 8"]
BARRIOS = ["San Fernando", "Granada", "Ciudad Jardín", "El Peñón", "Pance", "Chipichape"]

# (nombre, descripción, categoría, precio, stock, stock_mínimo)
PRODUCTOS = [
    ("Laptop Lenovo 15\"", "Intel i5, 8GB RAM, 512GB SSD", "Electrónica", 2450000, 12, 3),
    ("Mouse inalámbrico", "Sensor óptico 1600 DPI", "Electrónica", 45000, 60, 10),
    ("Teclado mecánico", "Switches rojos, retroiluminado", "Electrónica", 180000, 25, 5),
    ("Monitor 24\" Full HD", "Panel IPS, 75Hz", "Electrónica", 520000, 14, 4),
    ("Audífonos Bluetooth", "Cancelación de ruido", "Electrónica", 230000, 30, 6),
    ("Smartphone Galaxy A15", "128GB, cámara 50MP", "Electrónica", 890000, 18, 5),
    ("Tablet 10\"", "64GB, Wi-Fi", "Electrónica", 640000, 4, 5),
    ("Cargador USB-C 65W", "Carga rápida", "Electrónica", 95000, 40, 8),
    ("Webcam HD", "1080p con micrófono", "Electrónica", 120000, 3, 5),
    ("Disco duro externo 1TB", "USB 3.0", "Electrónica", 280000, 22, 5),
    ("Escritorio de oficina", "120x60 cm, melamina", "Muebles", 420000, 10, 3),
    ("Silla ergonómica", "Respaldo lumbar ajustable", "Muebles", 560000, 8, 3),
    ("Estantería de 5 niveles", "Madera aglomerada", "Muebles", 310000, 15, 4),
    ("Sofá de 3 puestos", "Tela antimanchas", "Muebles", 1450000, 5, 2),
    ("Mesa de comedor", "6 puestos, madera", "Muebles", 980000, 6, 2),
    ("Cama doble", "Con base y cabecero", "Muebles", 1250000, 2, 3),
    ("Mesa de noche", "Un cajón", "Muebles", 190000, 20, 5),
    ("Archivador metálico", "4 gavetas", "Muebles", 480000, 7, 2),
    ("Biblioteca modular", "Roble claro", "Muebles", 670000, 9, 3),
    ("Mesa de centro", "Vidrio templado", "Muebles", 340000, 11, 3),
]

ESTADOS = ["Pendiente", "Completada", "Completada", "Completada", "Cancelada"]


def limpiar():
    DetalleVenta.query.delete()
    Venta.query.delete()
    Producto.query.delete()
    Cliente.query.delete()
    db.session.commit()
    print("Datos anteriores eliminados.")


def crear_clientes():
    clientes = []
    for i, nombre in enumerate(NOMBRES):
        sin_tildes = (nombre.lower()
                      .replace("á", "a").replace("é", "e").replace("í", "i")
                      .replace("ó", "o").replace("ú", "u").replace("ñ", "n"))
        correo = ".".join(sin_tildes.split()[:2]) + "@correo.com"
        cliente = Cliente(
            nombre=nombre,
            direccion=f"{random.choice(CALLES)} #{random.randint(1, 99)}-{random.randint(1, 99)}, "
                      f"{random.choice(BARRIOS)}",
            telefono=f"3{random.randint(0, 2)}{random.randint(0, 9)}"
                     f"{random.randint(1000000, 9999999)}",
            email=correo,
        )
        db.session.add(cliente)
        clientes.append(cliente)
    db.session.commit()
    return clientes


def crear_productos():
    productos = []
    for nombre, desc, cat, precio, stock, minimo in PRODUCTOS:
        p = Producto(
            nombre=nombre, descripcion=desc, categoria=cat,
            precio=Decimal(precio), stock=stock, stock_minimo=minimo,
        )
        db.session.add(p)
        productos.append(p)
    db.session.commit()
    return productos


def crear_ventas(clientes, productos):
    # Los primeros 14 clientes (mezclados) tendrán ventas; los otros 6 no.
    con_ventas = random.sample(clientes, 14)
    total_ventas = 0

    for cliente in con_ventas:
        for _ in range(random.randint(1, 4)):
            disponibles = [p for p in productos if p.stock > 0]
            if not disponibles:
                break

            venta = Venta(
                id_cliente=cliente.id_cliente,
                fecha=date.today() - timedelta(days=random.randint(0, 120)),
                estado=random.choice(ESTADOS),
                total=Decimal("0"),
            )
            db.session.add(venta)

            subtotal_venta = Decimal("0")
            elegidos = random.sample(disponibles, min(len(disponibles), random.randint(1, 4)))
            for producto in elegidos:
                cantidad = random.randint(1, min(3, producto.stock))
                subtotal = producto.precio * cantidad
                db.session.add(DetalleVenta(
                    venta=venta,
                    id_producto=producto.id_producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio,
                    subtotal=subtotal,
                ))
                producto.stock -= cantidad
                subtotal_venta += subtotal

            # Descuento ocasional del 5% o 10%
            descuento = random.choice([0, 0, 5, 10])
            venta.total = subtotal_venta * (Decimal(100 - descuento) / Decimal(100))
            total_ventas += 1

    db.session.commit()
    return con_ventas, total_ventas


def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        if "--reset" in sys.argv:
            limpiar()

        clientes = crear_clientes()
        productos = crear_productos()
        con_ventas, n_ventas = crear_ventas(clientes, productos)

        print(f"Clientes creados:   {len(clientes)} ({len(con_ventas)} con ventas, "
              f"{len(clientes) - len(con_ventas)} sin ventas)")
        print(f"Productos creados:  {len(productos)}")
        print(f"Ventas creadas:     {n_ventas}")


if __name__ == "__main__":
    main()
