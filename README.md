# demo-catalogocojines

Aplicación Flask que muestra el catálogo en PDF para el stack `1` consultando la vista `vista_catalogo_stack1` en PostgreSQL. La página principal lista todos los catálogos disponibles para ese stack, permite seleccionar uno por nombre y muestra:

- Portada del catálogo como fondo del encabezado (`url_portada`).
- Título con el `catalog_name` y subtítulo con la `description`.
- Botón “Abrir catálogo en nueva pestaña”.

La vista `vista_catalogo_stack1` debe exponer:

- `catalog_id`, `catalog_name`, `collection`, `description`, `stack`, `url_catalogo`, `url_portada`.

Rutas principales:

- `/` página con selector por nombre para el stack 1.
- `/stack/<id>` tabla básica para cualquier stack.

## Requisitos Previos

- Docker y Docker Compose (v2 o superior).
- Python 3.10+ si deseas ejecutar sin contenedores.
- Una base PostgreSQL accesible con la vista `6`.

## Variables de Entorno

- `DATABASE_URL` (obligatoria): cadena de conexión a PostgreSQL.
  - Formato: `postgresql://usuario:password@host:5432/base`
- Variables ya definidas en Dockerfile para ejecutar Flask dentro del contenedor: `FLASK_APP=app.main:app`, `FLASK_RUN_HOST=0.0.0.0`, `FLASK_RUN_PORT=5000`.

Puedes definir `DATABASE_URL` de dos formas:

1) Archivo `.env` en la raíz del proyecto (lo leerá Docker Compose):

```env
DATABASE_URL=postgresql://usuario:password@host:5432/base
```

2) Exportándola manualmente en tu terminal para ejecución local.

PowerShell (Windows):

```powershell
$env:DATABASE_URL = "postgresql://admin:admin123@172.21.0.8:5432/cojines"
```

Linux/macOS (bash):

```bash
export DATABASE_URL="postgresql://usuario:password@host:5432/base"
```

## Ejecutar con Docker Compose

1) Asegúrate de tener `DATABASE_URL` disponible (en `.env` o variable de entorno).

2) Construye y levanta el servicio:

```powershell
docker compose up --build -d
```

3) Abre la app en el navegador: http://localhost:8800

4) Detener servicios:

```powershell
docker compose down
```

Nota: el `docker-compose.yml` mapea el puerto del contenedor `5000` al `8800` del host.

## Build y Push a un Registry (PowerShell)

Los siguientes comandos asumen que tienes un registro de contenedores (Docker Hub, ACR, GHCR, etc.). Personaliza y ejecuta en PowerShell:

```powershell
# Variables de despliegue
$REGISTRY = "docker.io"              # ej. docker.io, ghcr.io, miacr.azurecr.io
$NAMESPACE = "erifcamp"              # opcional según el registry
$IMAGE = "demo-catalogocojines"
$TAG = "v1.0"                        # o "latest"

# Nombre completo de la imagen
if ($NAMESPACE) {
  $FULL = "${REGISTRY}/${NAMESPACE}/${IMAGE}:${TAG}"
} else {
  $FULL = "${REGISTRY}/${IMAGE}:${TAG}"
}

# 1) Login (puede pedir usuario/token)
docker login $REGISTRY

# 2) Build de la imagen
docker build -t $FULL .

# 3) Push al registry
docker push $FULL

# 4) (Opcional) Ejecutar la imagen publicada en cualquier host
#    Requiere pasar DATABASE_URL y mapear puertos
docker run --rm -e DATABASE_URL=$env:DATABASE_URL -p 8800:5000 $FULL

```

Sugerencia: también puedes etiquetar y subir `latest` además del tag versionado:

```powershell
$LATEST = $FULL -replace ":$TAG", ":latest"
docker tag $FULL $LATEST
docker push $LATEST
```

## Ejecución Local (sin Docker, opcional)

1) Crear y activar entorno virtual:

```powershell
python -m venv .venv
./.venv/Scripts/Activate.ps1
```

2) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

3) Definir `DATABASE_URL` y ejecutar Flask:

```powershell
$env:DATABASE_URL = "postgresql://admin:admin123@172.21.0.8:5432/base"
flask --app app.main run --debug
```

Abrir: http://localhost:5000

