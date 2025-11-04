"""Flask application for listing catalog entries filtered by stack.

Implements:
- Página principal (stack 1) con selector de catálogos por nombre.
- Actualiza el PDF mostrado al seleccionar un catálogo.
- Expone también `/stack/<id>` para ver cualquier stack en tabla.
"""

from __future__ import annotations

from flask import Flask, abort, jsonify, render_template, request
import logging
import os
from collections import deque
from datetime import datetime, timezone

try:
    from opencensus.ext.azure.log_exporter import AzureLogHandler  # type: ignore
except Exception:  # pragma: no cover
    AzureLogHandler = None  # Fallback if not installed

from .db import get_cursor


def create_app() -> Flask:
    app = Flask(__name__)

    # ---- Telemetry setup (logs only; no persistence on server) ----
    app.recent_events = deque(maxlen=200)  # type: ignore[attr-defined]

    logger = logging.getLogger("telemetry")
    logger.setLevel(logging.INFO)
    # Always log to console (Docker collects stdout)
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(sh)

    # Use connection string or instrumentation key from env
    conn_str = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")
    ikey = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY") or os.environ.get("APPLICATIONINSIGHTS_INSTRUMENTATIONKEY")
    if not conn_str and ikey:
        conn_str = f"InstrumentationKey={ikey}"
    # Attach Azure handler if available and configured
    telemetry_enabled = False
    if AzureLogHandler and conn_str:
        try:
            logger.addHandler(AzureLogHandler(connection_string=conn_str))
            telemetry_enabled = True
        except Exception:
            # Avoid crashing app if handler fails to init
            telemetry_enabled = False

    app.config["TELEMETRY_ENABLED"] = telemetry_enabled

    def client_ip() -> str:
        fwd = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        return fwd or request.remote_addr or ""

    def add_event(kind: str, message: str, **props):
        event = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "kind": kind,
            "ip": client_ip(),
            "ua": request.headers.get("User-Agent", ""),
            "path": request.path,
            "method": request.method,
            "ref": request.headers.get("Referer", ""),
            "msg": message,
            "props": props,
        }
        # Keep minimal in memory buffer (not used for UI)
        app.recent_events.appendleft(event)  # type: ignore[attr-defined]
        # Build a readable line for console (Docker logs)
        line_parts = [
            message,
            f"ip={event['ip']}",
            f"path={event['path']}",
        ]
        if props.get("catalog_id") is not None:
            line_parts.append(f"catalog_id={props['catalog_id']}")
        if props.get("catalog_name"):
            line_parts.append(f"catalog={props['catalog_name']}")
        if props.get("href"):
            line_parts.append(f"href={props['href']}")
        log_line = f"{kind} " + " ".join(line_parts)
        # Emit to console and Azure (if enabled)
        try:
            logger.info(log_line, extra={"custom_dimensions": event})
        except Exception:
            pass

    @app.before_request
    def _log_request() -> None:
        # Skip noisy health/static endpoints if any in future
        add_event("view", "page_view")

    @app.route("/")
    def show_stack_one() -> str:
        """Render all entries for stack 1 as individual cards."""
        query = (
            "SELECT catalog_id, catalog_name, collection, description, stack, url_catalogo, url_portada, url_cartula "
            "FROM vista_catalogo_stack1 WHERE stack = %s ORDER BY catalog_id"
        )

        with get_cursor() as cursor:
            cursor.execute(query, (1,))
            rows = cursor.fetchall()

        if not rows:
            abort(404, description="No se encontró información para el stack 1.")

        hero = next((r.get("url_portada") for r in rows if r.get("url_portada")), None)

        return render_template(
            "stack_one.html",
            rows=rows,
            hero=hero,
            telemetry_enabled=app.config.get("TELEMETRY_ENABLED", False),
        )

    # Endpoint to receive client-side click logs
    @app.post("/log/click")
    def log_click():
        data = request.get_json(silent=True) or {}
        add_event(
            "click",
            data.get("message") or "click",
            target=data.get("target"),
            catalog_id=data.get("catalog_id"),
            catalog_name=data.get("catalog_name"),
            href=data.get("href"),
        )
        return ("", 204)

    # (Removed UI polling endpoint; logs now go to stdout and Azure only)

    def index() -> str:
        """Show a simple landing page with usage instructions."""
        return render_template("index.html")

    @app.route("/stack/<int:stack_id>")
    def show_stack(stack_id: int) -> str:
        """Render the catalog entries associated with the given stack."""
        query = (
            "SELECT catalog_id, catalog_name, collection, stack, url_catalogo, url_portada, url_cartula "
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
