"""Flask application that displays the PDF for stack 1."""

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

    return app


app = create_app()
