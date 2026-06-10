"""
Eco-Distribuidora S.A. - Sistema CRUD Legacy
=============================================
Sistema de gestión de inventario básico (Flask + SQLite).
NOTA DE AUDITORÍA: Este sistema es intencionalmente "pobre" para la toma
de decisiones. Ver /docs/INFORME_AUDITORIA.md para el análisis completo.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "eco-distribuidora-secret"
DATABASE = "eco_distribuidora.db"


# ──────────────────────────────────────────────────────────
# Utilidad de conexión
# ──────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Crea las tablas si no existen."""
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS productos (
                id_producto      INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre           TEXT    NOT NULL,
                descripcion      TEXT,
                precio_unitario  REAL    NOT NULL DEFAULT 0,
                stock_actual     INTEGER NOT NULL DEFAULT 0,
                categoria        TEXT,
                fecha_ingreso    TEXT
            );

            CREATE TABLE IF NOT EXISTS ventas (
                id_venta        INTEGER PRIMARY KEY AUTOINCREMENT,
                id_producto     INTEGER,
                nombre_cliente  TEXT,
                cantidad        INTEGER NOT NULL DEFAULT 1,
                total_venta     REAL,
                fecha_venta     TEXT,
                vendedor        TEXT
            );
        """)


# ──────────────────────────────────────────────────────────
# INICIO
# ──────────────────────────────────────────────────────────
@app.route("/")
def index():
    db = get_db()
    total_productos = db.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    total_ventas    = db.execute("SELECT COUNT(*) FROM ventas").fetchone()[0]
    # Sin cálculos estratégicos - sólo conteos planos
    return render_template("index.html",
                           total_productos=total_productos,
                           total_ventas=total_ventas)


# ──────────────────────────────────────────────────────────
# PRODUCTOS - CRUD completo
# ──────────────────────────────────────────────────────────
@app.route("/productos")
def productos():
    db = get_db()
    # Devuelve TODOS los registros sin paginación ni filtros analíticos
    rows = db.execute("SELECT * FROM productos ORDER BY id_producto").fetchall()
    return render_template("productos.html", productos=rows)


@app.route("/productos/nuevo", methods=["GET", "POST"])
def nuevo_producto():
    if request.method == "POST":
        db = get_db()
        db.execute(
            """INSERT INTO productos
               (nombre, descripcion, precio_unitario, stock_actual, categoria, fecha_ingreso)
               VALUES (?, ?, ?, ?, ?, date('now'))""",
            (
                request.form["nombre"],
                request.form["descripcion"],
                float(request.form["precio_unitario"]),
                int(request.form["stock_actual"]),
                request.form["categoria"],
            ),
        )
        db.commit()
        flash("Producto creado correctamente.", "success")
        return redirect(url_for("productos"))
    return render_template("producto_form.html", producto=None)


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    db = get_db()
    producto = db.execute("SELECT * FROM productos WHERE id_producto=?", (id,)).fetchone()
    if not producto:
        flash("Producto no encontrado.", "error")
        return redirect(url_for("productos"))

    if request.method == "POST":
        db.execute(
            """UPDATE productos SET nombre=?, descripcion=?, precio_unitario=?,
               stock_actual=?, categoria=? WHERE id_producto=?""",
            (
                request.form["nombre"],
                request.form["descripcion"],
                float(request.form["precio_unitario"]),
                int(request.form["stock_actual"]),
                request.form["categoria"],
                id,
            ),
        )
        db.commit()
        flash("Producto actualizado.", "success")
        return redirect(url_for("productos"))
    return render_template("producto_form.html", producto=producto)


@app.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    db = get_db()
    db.execute("DELETE FROM productos WHERE id_producto=?", (id,))
    db.commit()
    flash("Producto eliminado.", "success")
    return redirect(url_for("productos"))


# ──────────────────────────────────────────────────────────
# VENTAS - CRUD completo
# ──────────────────────────────────────────────────────────
@app.route("/ventas")
def ventas():
    db = get_db()
    # JOIN básico pero sin análisis: devuelve tabla interminable
    rows = db.execute("""
        SELECT v.*, p.nombre AS nombre_producto
        FROM ventas v
        LEFT JOIN productos p ON v.id_producto = p.id_producto
        ORDER BY v.id_venta DESC
    """).fetchall()
    return render_template("ventas.html", ventas=rows)


@app.route("/ventas/nueva", methods=["GET", "POST"])
def nueva_venta():
    db = get_db()
    productos_lista = db.execute("SELECT id_producto, nombre, precio_unitario FROM productos").fetchall()

    if request.method == "POST":
        cantidad   = int(request.form["cantidad"])
        id_prod    = int(request.form["id_producto"])
        precio_row = db.execute("SELECT precio_unitario FROM productos WHERE id_producto=?", (id_prod,)).fetchone()
        total      = round(precio_row["precio_unitario"] * cantidad, 2) if precio_row else 0

        db.execute(
            """INSERT INTO ventas
               (id_producto, nombre_cliente, cantidad, total_venta, fecha_venta, vendedor)
               VALUES (?, ?, ?, ?, date('now'), ?)""",
            (id_prod, request.form["nombre_cliente"], cantidad, total, request.form["vendedor"]),
        )
        # FALLA INTENCIONAL: el stock NO se actualiza automáticamente
        # Esto ilustra la falta de integridad referencial y sinergia entre tablas
        db.commit()
        flash("Venta registrada. (AVISO: el stock no se actualiza automáticamente)", "warning")
        return redirect(url_for("ventas"))
    return render_template("venta_form.html", productos=productos_lista)


@app.route("/ventas/eliminar/<int:id>")
def eliminar_venta(id):
    db = get_db()
    db.execute("DELETE FROM ventas WHERE id_venta=?", (id,))
    db.commit()
    flash("Venta eliminada.", "success")
    return redirect(url_for("ventas"))


# ──────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(DATABASE):
        init_db()
    else:
        init_db()  # idempotente con CREATE TABLE IF NOT EXISTS
    app.run(debug=True, port=5000)
