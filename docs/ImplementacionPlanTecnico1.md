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

## 3. Bloque A ejecutable — COMPLETADO

Estado: todos los pasos A1-A10 implementados y validados.

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

## 5. Beta 1 ejecutable — COMPLETADA

Login, registro, perfil básico, sesión estable y admin funcional. 35 tests pasando.

## 6. Bloque C ejecutable — COMPLETADO

Estado: todos los pasos C1-C9 implementados y validados. 28 tests nuevos, 63 en total.

### Paso C1. Crear la app collections

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

## 7. Bloque D ejecutable — COMPLETADO

Estado: todos los pasos D1-D6 implementados y validados. 13 tests nuevos, 76 en total.

Dependencia instalada: nudenet 3.4.2 (clasificador local de contenido inapropiado, sin envio a terceros).

### Paso D1. Preparar imagenes y caratulas — COMPLETADO

El campo `cover` (ImageField) ya existe en CollectionItem desde el Bloque C.
No se ha separado en modelo propio; la primera version lo mantiene embebido.

### Paso D2. Implementar subida segura — COMPLETADO

Archivo: apps/collections/validators.py

Validaciones implementadas en orden:

1. Extension del archivo: solo jpg, jpeg, png, webp.
2. Tipo MIME real: leer cabecera de bytes con Pillow, no confiar en la extension.
3. Tamaño maximo: 5 MB.
4. Dimensiones: minimo 100x100 px, maximo 4000x4000 px.
5. Renombrado con UUID: el nombre original nunca llega al disco.
6. NudeNet: clasificador local; si detecta contenido explicito con score >= 0.6, rechaza con ValidationError.

Conexion con el modelo:

- El validator se añade al campo `cover` de CollectionItem.
- El formulario CollectionItemForm lo activa automaticamente.
- El error aparece en el formulario antes de guardar, sin persistir el archivo.

### Paso D3. Asociar imagenes a elementos — COMPLETADO

- CollectionItemForm tiene el campo cover.
- item_form.html usa enctype="multipart/form-data".
- Los elementos se muestran con caratula en collection_detail.html y en el listado.
- Los elementos sin caratula muestran un placeholder con CSS.

### Paso D4. Mejorar interfaz — COMPLETADO

- Grid de cards para colecciones e items en static/css/main.css.
- Badges de categoria y visibilidad.
- Layout coherente en listados y detalle.

### Paso D5. Accesibilidad minima — COMPLETADO

- Alt text descriptivo en todas las imagenes: "Caratula de {item.name}".
- Semantica HTML: article, section, nav, aria-labelledby, role="list".
- Placeholders accesibles para elementos sin caratula.

### Paso D6. Probar el bloque D — COMPLETADO

Archivo: apps/collections/tests/test_validators.py (13 tests)

Cobertura:

- imagen valida pasa todos los validators;
- extension no permitida rechazada;
- tipo MIME falso rechazado;
- imagen mayor de 5 MB rechazada;
- imagen exactamente en el limite aceptada;
- dimensiones pequeñas rechazadas;
- dimensiones grandes rechazadas;
- dimensiones validas aceptadas;
- NudeNet score alto rechaza imagen (mock sin red);
- NudeNet sin detecciones acepta imagen (mock);
- NudeNet score bajo acepta imagen (mock);
- NudeNet no instalado no bloquea la subida (mock ImportError).

## 8. Beta 2 ejecutable — COMPLETADA

Bloque D completado. 76 tests pasando. 0 errores ruff.

Criterios de cierre cumplidos:

- no hay fugas de ownership (6 tests de ownership pasando);
- la subida de imagenes esta asegurada con validators + NudeNet (13 tests);
- las reglas de identidad son estables (35 tests de users pasando).

Demo manual realizada: registro → login → colecciones → grupos → elementos → carátulas → navegación coherente.

## 9. Bloque E (parcial) — IMPLEMENTADO

Las siguientes funcionalidades del Bloque E están implementadas, validadas y con gate premium real.

### E-parcial 1. CollectionGroup — COMPLETADO (migración 0002)

Modelo CollectionGroup en apps/collections/models.py:

- collection (FK a Collection, CASCADE)
- name, slug (único por colección, auto-slugify)
- description (opcional)
- position (ordenación manual)
- created_at, updated_at

FK group en CollectionItem (SET_NULL, null=True, blank=True).

CRUD completo con ownership enforcement:
- group_create, group_detail, group_edit, group_delete en views.py
- Sugerencias de nombres predefinidas por categoría en suggestions.py
- Templates: group_form.html, group_detail.html, group_confirm_delete.html
- Selectors: get_groups_for_collection, get_group_for_collection, get_ungrouped_items
- Services: create_group, update_group
- Admin: CollectionGroupInline, CollectionGroupAdmin

Vista collection_detail muestra:
- Sección "Grupos" (listado de grupos con acciones)
- Sección "Sin grupo" (solo items con group=None)

Vista group_detail muestra dos listas:
- "Lo que tengo" (status=owned)
- "Lista de deseos" (status=wanted)

Pendiente: gate premium real implementado en la sesión siguiente (ver E-parcial 5).

### E-parcial 2. Mover y copiar contenido — COMPLETADO

Implementado en services.py, views.py y urls.py.

Operaciones disponibles:

1. **Mover elemento** (`/<col>/items/<item>/mover/`)
   - Mueve el elemento a otra colección y/o grupo del mismo usuario.
   - Si el nombre ya existe en destino: aviso con fusión de cantidades, requiere confirmación explícita.

2. **Mover grupo** (`/<col>/grupos/<grupo>/mover/`)
   - Mueve el grupo completo con todos sus elementos a otra colección.
   - Detecta duplicados de nombres en destino, pide confirmación.

3. **Transferir colección** (`/<col>/transferir/`)
   - Mover: todos los grupos e items pasan al destino, la colección origen queda vacía.
   - Copiar: se duplican en destino; la colección origen no cambia.
   - Detecta duplicados de nombres en destino, pide confirmación.

Lógica anti-duplicado:
- Función get_conflicts() detecta colisiones de nombre antes de ejecutar.
- En colisión: se muestra pantalla intermedia con el resultado previsto (suma de cantidades).
- El usuario confirma o cancela. Solo se fusionan si confirma.

### E-parcial 3. Campo quantity en CollectionItem — COMPLETADO (migración 0003)

- Campo quantity (PositiveIntegerField, default=1) añadido a CollectionItem.
- Visible y editable en CollectionItemForm (no obligatorio, default=1 si no se envía).
- Badge visual "x2", "x3"... en cards cuando quantity > 1.
- En admin: visible en inline y en CollectionItemAdmin list_display.

### E-parcial 4. Calidad de código — COMPLETADO

- Indentación 4 espacios en todos los archivos HTML.
- Copyright estandarizado en todos los .py y .html (2 líneas exactas).
- Sin BOM UTF-8 en ningún archivo.
- 76 tests, 0 errores ruff, 0 issues Django check.

### E-parcial 5. App billing y gate premium real — COMPLETADO (migración billing/0001)

Nueva app `apps/billing`:

- Modelo `Plan`: code, name, tier (free/premium), límites (max_collections, max_items_total,
  max_storage_bytes), funcionalidades (can_use_groups, can_upload_custom_images, etc.), timestamps.
- Modelo `Subscription`: user, plan, status (active/suspended/canceled/expired), fechas de periodo,
  grace_until, campos de pasarela externa para futuro, auto_renew.
- Servicio `user_can_use_groups(user)`: staff → True; suscripción activa con plan.can_use_groups → True; resto → False.
- Admin registrado para Plan y Subscription.

Gate en `group_create` (apps/collections/views.py):

- Si `user_can_use_groups` devuelve False → redirect a collection_detail con mensaje de error.
- Si devuelve True → flujo normal de creación.

85 tests pasando, 0 errores ruff.

### E-parcial 6. Navegación contextual en operaciones de elemento — COMPLETADO

Mejoras de UX para que las vistas de item respeten el contexto de grupo:

- `item_create`: acepta parámetro GET `?group=<slug>` para pre-seleccionar el grupo en el
  formulario. Tras guardar, si el item tiene grupo, redirige a `group_detail`; si no, a
  `collection_detail`.
- `item_edit`: tras guardar, redirige a `group_detail` si el item tiene grupo asignado.
- `item_delete`: guarda la referencia al grupo antes de borrar. Tras borrar, redirige a
  `group_detail` si el item tenía grupo.
- `group_detail.html`: botón "+ Añadir elemento" junto al encabezado de "Lo que tengo",
  con enlace `?group={{ group.slug }}` para pre-seleccionar el grupo.

85 tests pasando, 0 errores ruff.

## 10. Siguiente paso

Continuar en PlanTecnico2.md desde el Paso 44 (suspensión por impago) y Paso 48 (vistas de
cuenta/plan). El Paso 43 (modelar capacidades por plan) se considera cubierto con la implementación
de Plan.can_use_groups; ampliar límites numéricos cuando la UI de cuenta esté lista.
