# Implementacion Plan Tecnico 1

## 1. Objetivo

Este documento convierte PlanTecnico1.md en una guia de ejecucion real dentro del proyecto. La idea es que no haya que interpretar demasiado: se sigue en orden, se crean los archivos indicados, se validan los puntos de cierre y se pasa al siguiente paso.

Importante:

- Este documento cubre hasta Beta 2.
- No incluye la parte premium, suscripciones ni downgrade; eso queda para la segunda mitad.
- Para ejecutar estos pasos de verdad hace falta tener Python y Django disponibles en el entorno.

## 2. Precondiciones antes de empezar

1. Instalar Python en el sistema.
2. Confirmar que python o py funcionan desde terminal.
3. Definir version objetivo de Python.
4. Decidir si se usara requirements o pyproject como gestion principal.
5. Tener claro que la base de datos objetivo es PostgreSQL.

## 3. Bloque A ejecutable

### Paso A1. Crear la estructura raiz del repositorio

Crear esta estructura base:

- manage.py
- .env.example
- .gitignore
- README.md
- config/
- config/settings/
- apps/
- apps/common/
- apps/users/
- apps/collections/
- apps/audit/
- templates/
- static/
- media/
- tests/
- requirements/

Hecho cuando:

- existe una estructura clara y vacia preparada para llenarse;
- no hay dudas sobre donde ira cada modulo.

### Paso A2. Inicializar el proyecto Django

Tareas:

1. crear el proyecto principal;
2. mover la configuracion global a config;
3. dejar funcionando asgi, wsgi y urls.

Archivos esperados:

- config/__init__.py
- config/asgi.py
- config/wsgi.py
- config/urls.py
- config/settings/__init__.py

Hecho cuando:

- el proyecto arranca sin errores;
- la ruta principal responde.

### Paso A3. Separar settings por entorno

Crear:

- config/settings/base.py
- config/settings/local.py
- config/settings/test.py
- config/settings/production.py

Definir en base.py:

- INSTALLED_APPS base;
- MIDDLEWARE base;
- TEMPLATES;
- STATIC_URL;
- MEDIA_URL;
- AUTH_USER_MODEL provisional o definitivo si ya esta decidido;
- configuracion de logging base.

Definir overrides en cada entorno:

- local para desarrollo;
- test para tests;
- production para endurecimiento.

Hecho cuando:

- el proyecto puede arrancar en local;
- la seleccion del settings module es explicita;
- no hay configuracion productiva metida a mano en base.py.

### Paso A4. Preparar secretos y variables de entorno

Crear y documentar .env.example con variables como:

- DJANGO_SETTINGS_MODULE
- SECRET_KEY
- DEBUG
- ALLOWED_HOSTS
- DATABASE_URL o variables equivalentes
- EMAIL backend si se usa

Hecho cuando:

- el repositorio no contiene secretos reales;
- otra persona puede arrancar el proyecto copiando y rellenando el ejemplo.

### Paso A5. Configurar dependencias y herramientas

Definir dependencias base:

- Django
- psycopg
- Pillow
- django-environ o alternativa equivalente
- pytest
- pytest-django
- ruff

Si se usa requirements:

- requirements/base.txt
- requirements/local.txt
- requirements/test.txt
- requirements/production.txt

Hecho cuando:

- el proyecto se instala de manera repetible;
- las herramientas de calidad ya estan definidas.

### Paso A6. Configurar base de datos

Tareas:

1. dejar SQLite solo como opcion local si hace falta;
2. preparar PostgreSQL como objetivo real;
3. documentar claramente esta decision en README.

Hecho cuando:

- las migraciones futuras ya naceran pensando en PostgreSQL.

### Paso A7. Endurecer la configuracion basica

Aplicar en settings:

- ALLOWED_HOSTS por entorno;
- CSRF activo;
- X_FRAME_OPTIONS;
- SESSION_COOKIE_HTTPONLY;
- CSRF_COOKIE_HTTPONLY si el enfoque elegido lo justifica;
- SESSION_COOKIE_SECURE y CSRF_COOKIE_SECURE para production;
- SECURE_HSTS_SECONDS para production;
- SECURE_BROWSER_XSS_FILTER o equivalente moderno via cabeceras seguras;
- SECURE_CONTENT_TYPE_NOSNIFF.

Hecho cuando:

- el proyecto no nace en modo inseguro por defecto.

### Paso A8. Configurar logging y calidad automatica

Tareas:

1. crear logging minimo con consola y errores;
2. configurar ruff;
3. configurar pytest;
4. dejar preparado un comando de calidad.

Archivos esperados:

- pyproject.toml o configuracion equivalente
- pytest.ini si aplica

Hecho cuando:

- se pueden lanzar validaciones basicas de calidad.

### Paso A9. Crear base visual y recursos

Tareas:

1. crear templates/base.html;
2. crear estructura de static;
3. dejar layout inicial funcional;
4. preparar media para imagenes futuras.

Hecho cuando:

- ya existe una base de interfaz reutilizable.

### Paso A10. Documentar el bloque A

Actualizar README con:

- como instalar dependencias;
- como configurar variables;
- como arrancar;
- como lanzar tests;
- como lanzar linters.

Hecho cuando:

- una tercera persona puede arrancar el proyecto sin explicacion oral.

## 4. Bloque B ejecutable

### Paso B1. Crear la app users

Crear:

- apps/users/__init__.py
- apps/users/apps.py
- apps/users/models.py
- apps/users/admin.py
- apps/users/forms.py
- apps/users/views.py
- apps/users/urls.py
- apps/users/tests/

Hecho cuando:

- la app esta registrada y preparada para identidad.

### Paso B2. Implementar custom user model

Definir en apps/users/models.py:

- clase User personalizada;
- manager personalizado;
- email como identificador principal;
- campos minimos de identidad y seguridad.

Hecho cuando:

- AUTH_USER_MODEL apunta al modelo correcto;
- se pueden crear usuario y superusuario.

### Paso B3. Implementar perfil de usuario

Definir modelo Profile con:

- relacion uno a uno con User;
- avatar;
- zona horaria;
- idioma;
- campos de perfil no sensibles.

Hecho cuando:

- autenticacion y perfil quedan desacoplados.

### Paso B4. Implementar admin de usuarios

Tareas:

1. registrar User;
2. registrar Profile;
3. añadir list_display, search_fields y filtros utiles;
4. ocultar lo que no aporte operativamente.

Hecho cuando:

- soporte puede gestionar usuarios desde admin de forma razonable.

### Paso B5. Implementar registro, login y logout

Crear:

- formularios de registro y login;
- vistas de registro y autenticacion;
- plantillas de cuenta.

Plantillas previstas:

- templates/account/login.html
- templates/account/register.html
- templates/account/password_reset.html
- templates/account/password_change.html

Hecho cuando:

- un usuario puede crear cuenta y acceder.

### Paso B6. Endurecer autenticacion

Tareas:

1. añadir rate limiting;
2. definir validadores de contraseña;
3. preparar verificacion de email si entra en el alcance;
4. revisar expiracion y seguridad de sesiones.

Hecho cuando:

- la autenticacion ya no depende solo del happy path.

### Paso B7. Definir permisos y grupos base

Crear grupos:

- free
- premium
- staff

Definir permisos iniciales para:

- acceso a recursos propios;
- acceso administrativo minimo;
- futuras capacidades premium.

Hecho cuando:

- el backend ya tiene una base de autorizacion coherente.

### Paso B8. Crear auditoria basica de accesos

Si la app audit ya existe, integrar:

- login correcto;
- cambios de contraseña;
- eventos relevantes de identidad.

Si aun no existe, dejar una implementacion minima o una interfaz preparada para enchufarla.

Hecho cuando:

- los eventos sensibles de identidad dejan rastro.

### Paso B9. Probar el bloque B

Crear tests para:

- user model;
- profile;
- registro;
- login;
- logout;
- cambio y recuperacion de contraseña;
- permisos base.

Hecho cuando:

- la identidad del sistema esta defendida por pruebas.

## 5. Beta 1 ejecutable

Preparar una demo con:

- login;
- registro;
- perfil basico;
- sesion estable;
- admin util.

No pasar al siguiente bloque si:

- el login falla;
- el custom user no esta consolidado;
- los permisos base siguen ambiguos.

## 6. Bloque C ejecutable

### Paso C1. Crear la app collections

Crear:

- apps/collections/__init__.py
- apps/collections/apps.py
- apps/collections/models.py
- apps/collections/admin.py
- apps/collections/forms.py
- apps/collections/views.py
- apps/collections/urls.py
- apps/collections/selectors.py
- apps/collections/services.py
- apps/collections/tests/

Hecho cuando:

- la app del nucleo funcional esta preparada.

### Paso C2. Implementar Collection

Definir el modelo con:

- owner;
- name;
- slug;
- description;
- visibility;
- category;
- timestamps.

Hecho cuando:

- existe la entidad principal del producto.

### Paso C3. Implementar CollectionItem

Definir el modelo con:

- collection;
- name;
- slug opcional;
- description;
- personal_comment;
- status;
- position;
- timestamps.

Hecho cuando:

- existe la unidad principal de contenido.

### Paso C4. Definir constraints e indices

Aplicar:

- unicidad por owner y slug en colecciones;
- integridad relacional;
- indices para listados previsibles.

Hecho cuando:

- la base de datos ya protege reglas del dominio.

### Paso C5. Implementar formularios y vistas CRUD

Crear:

- formularios de coleccion;
- formularios de item;
- vistas de listado, detalle, alta, edicion y borrado.

Hecho cuando:

- el flujo principal del producto existe de punta a punta.

### Paso C6. Aplicar ownership real

Asegurar en vistas, servicios y consultas:

- que el usuario solo ve lo suyo;
- que no puede modificar objetos ajenos;
- que el admin respeta permisos especiales.

Hecho cuando:

- no existe exposicion cruzada de datos.

### Paso C7. Crear selectors y services utiles

Mover a selectors:

- listados optimizados;
- consultas reutilizables.

Mover a services:

- creacion con reglas de negocio;
- actualizacion con logica no trivial.

Hecho cuando:

- las vistas no concentran logica de negocio compleja.

### Paso C8. Mejorar admin del nucleo funcional

Añadir en admin:

- filtros;
- busquedas;
- listados utiles;
- restricciones de seguridad.

Hecho cuando:

- el nucleo tambien es operable desde admin.

### Paso C9. Probar el bloque C

Crear tests para:

- modelos;
- formularios;
- ownership;
- permisos;
- vistas principales.

Hecho cuando:

- el corazon funcional esta cubierto por pruebas.

## 7. Bloque D ejecutable

### Paso D1. Preparar imagenes y caratulas

Si se mantiene dentro de collections, implementar el modelo ahi. Si se separa, crear un modulo especifico de media.

Definir:

- relacion con item;
- archivo;
- origen;
- alt_text;
- mime_type;
- size;
- dimensiones;
- timestamps.

Hecho cuando:

- la imagen ya es una entidad controlada y no un campo improvisado.

### Paso D2. Implementar subida segura

Aplicar:

- validacion real de tipo;
- validacion de tamaño;
- validacion de dimensiones;
- nombres no predecibles;
- reprocesado si procede.

Hecho cuando:

- la subida de media no rompe la postura de seguridad.

### Paso D3. Asociar imagenes a elementos

Tareas:

1. integrar en formulario;
2. impedir asociaciones ajenas;
3. mostrar las caratulas en detalle y listado.

Hecho cuando:

- los elementos ya se presentan con apoyo visual.

### Paso D4. Mejorar interfaz y accesibilidad minima

Revisar:

- listados;
- detalles;
- texto alternativo;
- semantica HTML;
- claridad visual.

Hecho cuando:

- el producto ya es enseñable sin parecer un prototipo crudo.

### Paso D5. Probar el bloque D

Crear tests para:

- subida segura;
- permisos sobre imagenes;
- integracion visual principal.

Hecho cuando:

- la funcionalidad visual queda validada.

## 8. Beta 2 ejecutable

La demo cliente de Beta 2 debe incluir:

- registro y login;
- perfil basico;
- creacion de colecciones;
- gestion de elementos;
- caratulas;
- navegacion coherente.

No pasar a la segunda mitad del plan si:

- hay fugas de ownership;
- la subida de imagenes no esta asegurada;
- las reglas de identidad siguen inestables.

## 9. Siguiente paso natural

Tras cerrar Beta 2, continuar en PlanTecnico2.md y aplicar el modelo de datos definido para planes, suscripciones, suspension por impago, downgrade a free y estado excedido.
