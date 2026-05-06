# Colecciones

Aplicación web para gestionar colecciones personales. Construida con Django 6, arquitectura limpia y preparada para producción.

## Requisitos

- Python 3.13+
- pip

## Instalación

```bash
# Crear y activar entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements/local.txt

# Configurar variables de entorno
copy .env.example .env
# editar .env con los valores reales

# Aplicar migraciones
python manage.py migrate

# Arrancar servidor
python manage.py runserver
```

## Configuración por entorno

El módulo de settings se selecciona mediante la variable `DJANGO_SETTINGS_MODULE`:

| Entorno     | Módulo                        |
|-------------|-------------------------------|
| Local       | `config.settings.local`       |
| Test        | `config.settings.test`        |
| Producción  | `config.settings.production`  |

`manage.py` apunta a `local` por defecto.

## Tests

```bash
pytest
```

## Calidad de código

```bash
ruff check .
ruff format .
```

## Estructura

```
config/          configuración Django (urls, wsgi, asgi, settings/)
apps/            apps del proyecto (users, collections, audit, common)
templates/       plantillas HTML
static/          ficheros estáticos (css, js, img)
media/           ficheros subidos por usuarios
tests/           tests globales
requirements/    dependencias por entorno
```
