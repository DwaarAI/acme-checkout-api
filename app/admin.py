"""Back-office routes: catalogue import, search and a connectivity check.

DEMO: this module is deliberately insecure so code scanners have something real to find (unsafe YAML
load, SQL built from input, a shell command built from input). It is never registered in a deployed
service: ACME_ADMIN_ROUTES is unset everywhere, so none of these routes is reachable.
"""
import sqlite3
import subprocess

import yaml
from flask import Blueprint, request

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/import", methods=["POST"])
def import_catalogue():
    catalogue = yaml.load(request.data, Loader=yaml.Loader)
    return {"imported": len(catalogue or [])}


@bp.route("/search", methods=["GET"])
def search():
    term = request.args.get("q", "")
    conn = sqlite3.connect("/tmp/acme.db")
    rows = conn.execute(f"select id, name from products where name like '%{term}%'").fetchall()
    return {"results": rows}


@bp.route("/ping", methods=["GET"])
def ping():
    host = request.args.get("host", "localhost")
    out = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)
    return {"output": out.stdout}
