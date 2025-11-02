# demo-catalogocojines

Aplicación Flask sencilla que muestra los registros de la vista `vista_catalogo_sin_fechas` filtrados por el valor de `stack`.

## Requisitos

- Docker y Docker Compose.
- Una base de datos PostgreSQL accesible con la vista `vista_catalogo_sin_fechas` disponible.

## Configuración

Establece la variable de entorno `DATABASE_URL` con la cadena de conexión de tu base de datos, por ejemplo:

```bash
export DATABASE_URL="postgresql://usuario:password@host:5432/base"
```

## Ejecutar con Docker Compose

```bash
docker compose up --build
```

Una vez levantado el servicio, abre <http://localhost:5000> en tu navegador y navega a `/stack/<id>` para ver los catálogos de cada stack.
