# demo-catalogocojines

Aplicación Flask que muestra los registros de la vista `vista_catalogo_sin_fechas` filtrados por el valor de `stack`.

## Requisitos previos

- Docker y Docker Compose (v2 o superior).
- Python 3.10+ si deseas ejecutar la aplicación sin contenedores.
- Una base de datos PostgreSQL accesible con la vista `vista_catalogo_sin_fechas` disponible.

## Configurar la variable de entorno `DATABASE_URL`

La aplicación necesita la cadena de conexión a la base de datos en la variable `DATABASE_URL`, por ejemplo:

```bash
postgresql://usuario:password@host:5432/base
```

Puedes definirla de dos formas:

1. **Exportándola en tu terminal** (útil para desarrollo local):
   ```bash
   export DATABASE_URL="postgresql://usuario:password@host:5432/base"
   ```
2. **Creando un archivo `.env`** en la raíz del proyecto para que Docker Compose lo lea automáticamente:
   ```env
   DATABASE_URL=postgresql://usuario:password@host:5432/base
   ```

## Ejecutar con Docker Compose

1. Asegúrate de haber configurado `DATABASE_URL` (ya sea exportándola o con un archivo `.env`).
2. Construye y levanta el servicio:
   ```bash
   docker compose up --build
   ```
3. Abre <http://localhost:5000> en tu navegador y navega a `/stack/<id>` (por ejemplo `/stack/1`).

Para detener los contenedores:
```bash
docker compose down
```

## Ejecutar en un entorno virtual de Python (opcional)

1. Crea y activa un entorno virtual:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Define la variable `DATABASE_URL` como se describió antes.
4. Arranca la aplicación Flask:
   ```bash
   flask --app app.main run --debug
   ```
5. Abre <http://localhost:5000> en tu navegador.

Cuando termines, puedes desactivar el entorno virtual con `deactivate`.
