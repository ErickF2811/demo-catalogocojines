"""Flask application for listing catalog entries filtered by stack.

Implements:
- Página principal (stack 1) con selector de catálogos por nombre.
- Actualiza el PDF mostrado al seleccionar un catálogo.
- Expone también `/stack/<id>` para ver cualquier stack en tabla.
"""

from __future__ import annotations

from flask import Flask, abort, render_template, request

from .db import get_cursor


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def show_stack_one() -> str:
        """Render entries for stack 1 with selection by name only.

        Query params:
        - `id`: id del catálogo seleccionado (opcional)
        """
        query = (
            "SELECT catalog_id, catalog_name, collection, description, stack, url_catalogo, url_portada "
            "FROM vista_catalogo_stack1 WHERE stack = %s ORDER BY catalog_id"
        )

        with get_cursor() as cursor:
            cursor.execute(query, (1,))
            rows = cursor.fetchall()

        if not rows:
            abort(404, description="No se encontró información para el stack 1.")

        selected_id = request.args.get("id", type=int)
        selected = next((r for r in rows if r["catalog_id"] == selected_id), rows[0])

        return render_template("stack_one.html", rows=rows, selected=selected)

    def index() -> str:
        """Show a simple landing page with usage instructions."""
        return render_template("index.html")

    @app.route("/stack/<int:stack_id>")
    def show_stack(stack_id: int) -> str:
        """Render the catalog entries associated with the given stack."""
        query = (
            "SELECT catalog_id, catalog_name, collection, stack, url_catalogo, url_portada "
            "FROM vista_catalogo_stack1 WHERE stack = %s ORDER BY catalog_id"
        )

        with get_cursor() as cursor:
            cursor.execute(query, (stack_id,))
            rows = cursor.fetchall()

        if not rows:
            abort(404, description="No se encontraron resultados para el stack solicitado.")

        return render_template("stack.html", stack_id=stack_id, rows=rows)

    return app


app = create_app()
