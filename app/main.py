"""Acme Checkout API: the catalogue and orders behind the Acme storefront."""
import os
import sqlite3

from flask import Flask, jsonify, request

from app import settings

app = Flask(__name__)
DB = os.environ.get("ACME_DB", "/tmp/acme.db")

PRODUCTS = [
    (1, "Trail runner shoes", 89.0),
    (2, "Merino base layer", 64.0),
    (3, "Insulated bottle", 29.0),
    (4, "Headlamp 400lm", 39.0),
]


def db():
    conn = sqlite3.connect(DB)
    conn.execute("create table if not exists products (id integer primary key, name text, price real)")
    if not conn.execute("select count(*) from products").fetchone()[0]:
        conn.executemany("insert into products values (?, ?, ?)", PRODUCTS)
        conn.commit()
    return conn


@app.route("/health", methods=["GET"])
def health():
    return {"ok": True, "service": "acme-checkout-api", "version": settings.VERSION}


@app.route("/api/products", methods=["GET"])
def products():
    rows = db().execute("select id, name, price from products order by id").fetchall()
    return jsonify([{"id": r[0], "name": r[1], "price": r[2]} for r in rows])


@app.route("/api/products/<int:product_id>", methods=["GET"])
def product(product_id):
    row = db().execute("select id, name, price from products where id = ?", (product_id,)).fetchone()
    if not row:
        return {"error": "not found"}, 404
    return {"id": row[0], "name": row[1], "price": row[2]}


@app.route("/api/orders", methods=["POST"])
def order():
    body = request.get_json(silent=True) or {}
    return {"accepted": True, "items": len(body.get("items", [])), "currency": settings.CURRENCY}, 202


if settings.ADMIN_ROUTES:
    # Back-office routes. Off in every deployment; see app/admin.py.
    from app import admin

    app.register_blueprint(admin.bp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
