
"""Flask application for listing catalog entries filtered by stack."""


from __future__ import annotations

from flask import Flask, abort, render_template

from .db import get_cursor


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")

    def show_stack_one() -> str:
        """Render the catalog entry associated with stack 1."""
        query = (
            "SELECT catalog_id, catalog_name, collection, stack, url_catalogo "
            "FROM vista_catalogo_sin_fechas "
            "WHERE stack = %s "
            "ORDER BY catalog_id LIMIT 1"
        )

        with get_cursor() as cursor:
            cursor.execute(query, (1,))
            row = cursor.fetchone()

        if row is None:
            abort(404, description="No se encontró información para el stack 1.")

        return render_template("stack_one.html", row=row)

    def index() -> str:
        """Show a simple landing page with usage instructions."""
        return render_template("index.html")

    @app.route("/stack/<int:stack_id>")
    def show_stack(stack_id: int) -> str:
        """Render the catalog entries associated with the given stack."""
        query = (
            "SELECT catalog_id, catalog_name, collection, stack, url_catalogo "
            "FROM vista_catalogo_sin_fechas WHERE stack = %s ORDER BY catalog_id"
        )

        with get_cursor() as cursor:
            cursor.execute(query, (stack_id,))
            rows = cursor.fetchall()

        if not rows:
            abort(404, description="No se encontraron resultados para el stack solicitado.")

        return render_template("stack.html", stack_id=stack_id, rows=rows)


    return app


app = create_app()
