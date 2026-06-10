"""
Script de inicialización de la base de datos.
Ejecutar una sola vez antes de arrancar la aplicación.
Uso: python init_db.py
"""

import sqlite3
import os

DATABASE = "eco_distribuidora.db"


def init_and_populate():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"[INFO] Base de datos anterior eliminada: {DATABASE}")

    conn = sqlite3.connect(DATABASE)

    with open("populate_db.sql", "r", encoding="utf-8") as f:
        sql = f.read()

    conn.executescript(sql)
    conn.commit()

    # Verificar
    productos = conn.execute("SELECT COUNT(*) FROM productos").fetchone()[0]
    ventas    = conn.execute("SELECT COUNT(*) FROM ventas").fetchone()[0]
    conn.close()

    print(f"[OK] Base de datos creada: {DATABASE}")
    print(f"     Productos insertados: {productos}")
    print(f"     Ventas insertadas:    {ventas}")
    print(f"\n[!] Notas de auditoría:")
    print(f"     - Los clientes tienen variantes de nombre (entropía)")
    print(f"     - El stock NO fue descontado tras las ventas (falta de sinergia)")
    print(f"     - Las fechas están como TEXT, no como tipo DATE")
    print(f"\nEjecuta 'python app.py' para iniciar el servidor.")


if __name__ == "__main__":
    init_and_populate()
