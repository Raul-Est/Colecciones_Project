# Domain

## 1. Visión del producto

Aplicación web para gestionar colecciones personales con una base arquitectónica preparada para producción real. El producto debe permitir a un usuario autenticado organizar sus colecciones de elementos como juegos, discos, libros u otros tipos de objetos coleccionables, manteniendo una experiencia limpia, segura, escalable y fácilmente mantenible.

La prioridad principal no es solo que funcione, sino que esté bien construido desde el primer día: seguridad por defecto, separación clara de responsabilidades, trazabilidad de acciones, cumplimiento de buenas prácticas de Django y una base sólida para evolucionar hacia un SaaS serio.

## 2. Objetivo funcional

Cada usuario podrá:

- Registrarse, autenticarse y gestionar su cuenta.
- Crear una o varias colecciones personales.
- Añadir elementos a cada colección.
- Asociar a cada elemento una carátula o imagen.
- Elegir entre subir una imagen propia o reutilizar una imagen ya disponible en el sistema si las reglas de negocio lo permiten.
- Añadir información descriptiva y comentarios personales.
- Consultar, editar y eliminar sus propios datos dentro de los límites definidos por permisos y políticas de retención.

El sistema deberá estar preparado para distinguir entre usuarios gratuitos, usuarios premium y administradores con distintos niveles de privilegio.

## 3. Principios rectores

Este proyecto se diseña con los siguientes principios no negociables:

- Seguridad primero.
- Arquitectura clara antes que rapidez improvisada.
- Código legible, testeable y mantenible.
- Regla DRY sin caer en abstracciones prematuras.
- Validación en todos los bordes de entrada.
- Mínimo privilegio en permisos y acceso a datos.
- Trazabilidad de operaciones sensibles.
- Separación estricta entre dominio, infraestructura y presentación.
- Configuración por entorno, nunca secretos hardcodeados.
- Preparación para producción desde el inicio.

## 4. Alcance funcional inicial

### 4.1 Incluido en la primera versión

- Gestión de usuarios autenticados.
- Perfil de usuario básico y ampliable.
- Gestión de roles base: free, premium y staff.
- Creación y gestión de colecciones.
- Creación y gestión de elementos dentro de una colección.
- Subida y selección de carátulas.
- Panel administrativo robusto para soporte y supervisión.
- Auditoría de acciones críticas.
- Base para facturación o control de suscripción premium.
- Fundamentos SEO para páginas públicas que puedan indexarse en el futuro.

### 4.2 No incluido inicialmente, pero previsto en diseño

- Pasarela de pago real.
- API pública para terceros.
- Compartición social de colecciones.
- Recomendaciones, rankings o motores inteligentes.
- Multitenancy complejo.
- Marketplace o compraventa.

## 5. Modelo de dominio

### 5.1 Entidades principales

#### Usuario

Representa a la persona autenticada dentro del sistema.

Datos recomendados:

- email como identificador principal.
- username opcional o derivado de reglas de producto.
- nombre.
- apellidos.
- fecha de nacimiento si realmente existe justificación legal y funcional.
- fecha de alta.
- estado de cuenta: activa, suspendida, pendiente de verificación, eliminada lógicamente.
- flags de seguridad: email verificado, MFA habilitado, último acceso, último cambio de contraseña.

Decisión importante:

- Usar un modelo de usuario personalizado desde el inicio mediante AUTH_USER_MODEL.
- Autenticación por email en lugar de depender del modelo User por defecto sin adaptar.

#### Perfil de usuario

Contiene datos de negocio no esenciales para autenticación.

Datos posibles:

- avatar.
- biografía corta.
- preferencias visuales o de privacidad.
- zona horaria.
- idioma.

Datos sensibles como direcciones físicas solo deben existir si hay un caso de uso real. Si no hay una necesidad funcional inmediata, no deben modelarse todavía.

#### Rol y permisos

La autorización debe apoyarse en grupos y permisos de Django, ampliados con reglas de negocio cuando sea necesario.

Roles base:

- free.
- premium.
- admin funcional.
- superadmin técnico solo si el entorno lo requiere.

Regla de diseño:

- Los roles no deben sustituir el sistema de permisos nativo de Django.
- Las decisiones sensibles deben comprobar permisos concretos, no solo nombres de rol.

#### Plan

Representa la oferta comercial aplicable a una cuenta en términos de capacidades, límites y funcionalidades.

Campos sugeridos:

- código interno.
- nombre comercial.
- tipo: free, premium u otros futuros.
- activo.
- orden de presentación.
- límites configurables.
- funcionalidades habilitadas.
- timestamps.

Reglas de negocio:

- El plan no debe modelarse como un simple texto o flag en el usuario.
- Los límites y privilegios deben depender del plan activo o del estado efectivo de la suscripción.
- El plan free debe existir como referencia explícita del dominio, aunque no requiera cobro.
- Los cambios de definición de un plan no deben implicar pérdida automática de datos del usuario.

#### Suscripción

Gestiona el estado premium del usuario.

Campos sugeridos:

- usuario.
- plan.
- fecha de inicio.
- fecha de renovación.
- fecha de fin.
- estado: activa, cancelada, vencida, suspendida.
- proveedor de pago externo si aplica en el futuro.

Reglas de negocio:

- La suscripción premium controla privilegios y límites, no la propiedad de los datos del usuario.
- Si una cuenta premium se suspende por impago, el usuario no pierde sus colecciones, elementos, imágenes ni historial asociado.
- En estado suspendido por impago, los datos quedan conservados e inaccesibles solo en aquello que dependa de privilegios premium, a la espera de reactivación del pago.
- Cuando el usuario regulariza el pago y la suscripción vuelve a estado activa, recupera automáticamente los privilegios premium compatibles con su plan sin necesidad de reconstruir datos.
- La suspensión por impago no debe provocar borrado físico ni borrado lógico automático de contenido del usuario.
- Los cambios de estado de la suscripción deben quedar auditados.

Reglas de downgrade de premium a free:

- Si un usuario deja de ser premium y pasa a free, pierde únicamente los privilegios premium y pasa a regirse por los límites del plan free.
- El sistema no debe borrar datos existentes por el mero cambio de plan.
- Si el usuario supera los límites del plan free por haber creado más contenido cuando era premium, su exceso de datos queda conservado pero bloqueado para nuevas ampliaciones incompatibles con free hasta que reduzca el uso o reactive premium.
- El usuario debe poder seguir consultando sus datos existentes, salvo que alguna capacidad premium específica requiera restricción funcional explícita.
- El sistema debe definir con claridad qué ocurre cuando un usuario free está por encima del límite permitido: por ejemplo, no podrá crear nuevas colecciones, nuevos elementos o nuevas cargas mientras siga excedido.
- La aplicación debe comunicar de forma clara y trazable cuándo un usuario está excedido respecto al plan free y qué opciones tiene para normalizar su estado.

Decisión de dominio importante:

- Los límites de capacidad por plan deben formar parte del dominio del producto y no quedar dispersos en la interfaz o en condicionales ad hoc.
- Conviene modelar explícitamente capacidades o límites del plan, por ejemplo número máximo de colecciones, número máximo de elementos, capacidad de almacenamiento o acceso a funcionalidades avanzadas.
- La transición entre estados de suscripción debe resolverse mediante reglas de negocio deterministas y testeables.

Concepto adicional de dominio:

- Debe existir una forma explícita de determinar si una cuenta está dentro de límites o en estado excedido respecto a su plan efectivo.
- El estado excedido no equivale a suspensión ni a eliminación de datos; significa que el usuario conserva información ya creada, pero no puede seguir ampliando capacidades bloqueadas por su plan actual.

#### Colección

Agrupa elementos de un usuario bajo una categoría o criterio personal.

Campos sugeridos:

- propietario.
- nombre.
- slug único por propietario.
- descripción.
- tipo principal: libros, juegos, discos, figuras, otros.
- visibilidad: privada, compartida, pública.
- timestamps.

Reglas:

- Un usuario solo puede gestionar sus propias colecciones salvo privilegios administrativos.
- El slug debe ser único por usuario, no necesariamente global.

#### Elemento de colección

Representa cada unidad coleccionable.

Campos sugeridos:

- colección.
- nombre.
- slug opcional o identificador amigable.
- descripción.
- comentario_personal opcional.
- estado del elemento: pendiente, activo, archivado.
- posición para ordenación manual.
- timestamps.

Reglas:

- No debe existir un elemento huérfano fuera de una colección.
- El comentario personal debe tratarse como contenido privado salvo decisión explícita de visibilidad.

#### Carátula o imagen

Representa una imagen asociada a un elemento.

Campos sugeridos:

- elemento.
- archivo.
- origen: subida_usuario, catálogo_interno.
- texto alternativo.
- hash del fichero para deduplicación si se desea.
- tipo MIME validado.
- tamaño.
- ancho y alto si se procesan.
- timestamps.

Reglas:

- Nunca confiar en la extensión del archivo.
- Validar tipo real, tamaño máximo y dimensiones razonables.
- Almacenar con nombres no predecibles.
- Separar media privada de pública si el modelo de permisos lo necesita.

#### Registro de auditoría

Entidad esencial para eventos sensibles.

Campos sugeridos:

- actor.
- acción.
- objeto afectado.
- tipo de objeto.
- timestamp.
- IP si hay base legal y política de privacidad.
- user agent resumido si aporta valor operativo.
- resultado: éxito, denegado, error.
- metadatos mínimos serializados.

Debe registrar, al menos:

- inicios de sesión.
- fallos repetidos de autenticación.
- cambios de contraseña.
- cambios de permisos.
- operaciones administrativas.
- cambios en suscripciones.
- eliminación o restauración de datos.

#### Evento financiero

No debe mezclarse con la lógica de colecciones. Debe vivir en un contexto separado si se implementa.

Campos sugeridos:

- tipo de movimiento.
- importe.
- moneda.
- usuario relacionado si aplica.
- referencia externa.
- estado.
- timestamps.

## 6. Requisitos de seguridad

La seguridad es un requisito estructural, no una mejora posterior.

### 6.1 Seguridad de autenticación

- Modelo de usuario personalizado desde el inicio.
- Contraseñas con hasher moderno de Django y política fuerte.
- Soporte preparado para MFA aunque no se active en la primera iteración.
- Verificación de email para operaciones sensibles.
- Rate limiting para login, recuperación de contraseña y endpoints sensibles.
- Bloqueo o mitigación progresiva ante intentos fallidos.
- Sesiones con configuración segura y expiración coherente.

### 6.2 Seguridad de autorización

- Todos los accesos a objetos deben filtrar por propietario o permiso explícito.
- Nunca confiar en identificadores enviados por el cliente sin revalidar ownership.
- Uso de mixins, servicios o policy objects para evitar duplicar chequeos.
- Principio de mínimo privilegio en admin, staff y tareas internas.

### 6.3 Seguridad de datos

- Minimización de datos personales.
- Separación entre datos de autenticación, perfil y finanzas.
- Cifrado en tránsito obligatorio.
- Cifrado en reposo para secretos y, si procede, para campos altamente sensibles fuera de la base estándar.
- No almacenar datos financieros sensibles si la pasarela externa puede asumir esa responsabilidad.
- Backups seguros y probados.

### 6.4 Seguridad de ficheros

- Validar contenido real de imágenes.
- Reprocesar imágenes subidas para eliminar contenido no esperado.
- No servir media privada directamente desde rutas inseguras.
- Limitar tamaño, formato y frecuencia de subida.
- Analizar la necesidad de escaneo antivirus si el riesgo crece.

### 6.5 Seguridad de aplicación Django

- CSRF activado.
- XSS mitigado mediante escape por defecto y plantillas seguras.
- Content Security Policy (CSP) configurada para restringir orígenes de scripts, estilos e imágenes. Es la defensa primaria contra XSS en navegadores modernos y no es sustituible por el escape de plantillas.
- Protección frente a clickjacking mediante X-Frame-Options.
- Cabeceras seguras en producción.
- HSTS en producción con `SECURE_HSTS_SECONDS` y `SECURE_HSTS_INCLUDE_SUBDOMAINS`.
- Cookies Secure, HttpOnly y SameSite.
- DEBUG siempre desactivado en producción.
- ALLOWED_HOSTS estrictamente definido.
- SECRET_KEY fuera del repositorio.
- Separación de settings por entorno.
- Páginas de error personalizadas (400, 403, 404, 500) que no expongan información interna del servidor.

### 6.6 Seguridad operativa

- Logs estructurados.
- Alertas sobre eventos anómalos.
- Auditoría de acciones críticas.
- Dependabot o estrategia equivalente para dependencias.
- Revisión continua de vulnerabilidades.
- Rotación de secretos.

## 7. Requisitos de calidad y buenas prácticas

### 7.1 Buenas prácticas de código

- Tipado estático progresivo donde aporte valor.
- Linters y formatters obligatorios.
- Tests automáticos desde el inicio.
- Servicios de dominio para lógica de negocio no trivial.
- Fat models y fat views no son aceptables si la lógica empieza a crecer.
- Formularios o serializers responsables de validación de entrada.
- Consultas optimizadas con select_related y prefetch_related cuando corresponda.
- Evitar señales para lógica crítica salvo casos muy justificados.

### 7.2 Buenas prácticas Django

- Apps cohesionadas por contexto funcional.
- Configuración desacoplada por entorno.
- Custom user model desde el día 0.
- Uso correcto de managers y querysets para reglas reutilizables.
- Admin realmente útil, no solo generado por defecto.
- Tests por app y por tipo de comportamiento.
- Migraciones limpias y pequeñas.

### 7.3 Buenas prácticas de estructura

- Separar dominio, aplicación e infraestructura sin caer en sobreingeniería.
- Mantener responsabilidades explícitas en cada módulo.
- Evitar utilidades genéricas sin propósito claro.
- Todo lo sensible debe tener una ruta clara de mantenimiento y pruebas.

## 8. Arquitectura propuesta

Estructura recomendada:

```text
colecciones_project/
├── manage.py
├── conftest.py                        # raíz pytest: activa Django setup para toda la suite
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml            # ejecuta ruff y formatter automáticamente antes de cada commit
├── docker-compose.yml                 # PostgreSQL local sin instalación manual en el host
├── Makefile                           # comandos frecuentes unificados: migrate, test, lint, shell
├── README.md
├── pyproject.toml
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   ├── wsgi.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── local.py
│       ├── test.py
│       └── production.py
├── apps/
│   ├── common/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── context_processors.py      # inyecta límites de plan activo en el contexto de cada plantilla
│   │   ├── exceptions.py              # excepciones de dominio centralizadas (QuotaExceeded, etc.)
│   │   ├── middleware/
│   │   │   ├── __init__.py
│   │   │   └── security.py            # cabeceras de seguridad adicionales y hooks de auditoría por request
│   │   ├── mixins.py
│   │   ├── models.py
│   │   ├── permissions.py             # clases IsOwner y similares para validar ownership en vistas
│   │   ├── storage.py                 # backend de almacenamiento seguro: valida MIME real, renombra ficheros
│   │   ├── validators.py
│   │   └── tests/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── backends.py                # backend de autenticación por email (AUTHENTICATION_BACKENDS)
│   │   ├── forms.py
│   │   ├── managers.py                # UserManager personalizado desacoplado del modelo
│   │   ├── models.py
│   │   ├── selectors.py
│   │   ├── services.py
│   │   ├── signals.py                 # crea Profile automáticamente al crear User (post_save)
│   │   ├── tokens.py                  # generador de tokens para verificación de email y reset
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── collections/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── admin.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── selectors.py
│   │   ├── services.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── billing/
│   │   ├── __init__.py
│   │   ├── admin.py                   # gestión de planes y suscripciones visible en el admin de Django
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── selectors.py               # consultas de cuota, estado de suscripción y límites por plan
│   │   ├── services.py
│   │   └── tests/
│   └── audit/
│       ├── __init__.py
│       ├── admin.py                   # visualización de AuditLog en el admin con filtros y búsqueda
│       ├── apps.py
│       ├── models.py
│       ├── services.py
│       └── tests/
├── templates/
│   ├── base.html
│   ├── account/
│   ├── collections/
│   ├── emails/                        # plantillas para correos transaccionales (verificación, reset, alertas)
│   └── errors/                        # páginas 400, 403, 404 y 500 personalizadas sin filtración de datos
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/
├── tests/
│   ├── integration/
│   └── e2e/
└── requirements/
    ├── base.txt
    ├── local.txt
    ├── test.txt
    └── production.txt
```

### 8.1 Justificación estructural

- `config` contiene solo configuración global.
- `apps` agrupa contextos funcionales reales.
- `common` solo debe contener piezas verdaderamente compartidas y estables.
- `collections` concentra el núcleo del producto.
- `users` separa autenticación, perfil y gestión de cuenta.
- `billing` aísla la parte económica.
- `audit` evita mezclar trazabilidad con lógica de negocio principal.

### 8.2 Justificación de las adiciones respecto a una estructura base mínima

**`conftest.py` en la raíz del proyecto**

pytest requiere este fichero en la raíz para configurar el entorno Django antes de ejecutar cualquier test. Sin él, los tests de apps internas no pueden importar modelos ni usar la base de datos de test.

**`docker-compose.yml`**

El dominio establece PostgreSQL como base de datos objetivo. Depender de una instalación manual de PostgreSQL en el host de cada desarrollador introduce inconsistencias y errores difíciles de diagnosticar. docker-compose garantiza que todos los entornos locales sean idénticos.

**`.pre-commit-config.yaml`**

ruff y el formatter están declarados como obligatorios en el dominio. Sin pre-commit, su ejecución depende de que cada desarrollador los recuerde antes de hacer commit. pre-commit los convierte en un paso automático no omitible.

**`Makefile`**

Centraliza comandos frecuentes como `make migrate`, `make test`, `make lint` y `make shell`. Evita que cada desarrollador tenga que recordar y escribir secuencias largas de comandos.

**`apps/common/permissions.py`**

El dominio exige que todos los accesos a objetos filtren por propietario o permiso explícito, y que nunca se confíe en identificadores enviados por el cliente sin revalidar ownership. Este fichero centraliza las clases `IsOwner` y similares para que todas las vistas las reutilicen de forma consistente, evitando duplicación y olvidos.

**`apps/common/storage.py`**

El dominio exige validar el contenido real de las imágenes, reprocesarlas para eliminar contenido no esperado y no servir media privada desde rutas inseguras. Estas reglas requieren un backend de almacenamiento personalizado que intercepte la escritura y el acceso a ficheros.

**`apps/common/middleware/`**

El rate limiting sobre endpoints sensibles y los hooks de auditoría por request necesitan un lugar explícito. Un paquete de middleware en common permite añadir, reutilizar y testear esta lógica sin contaminar otras apps.

**`apps/common/exceptions.py`**

Centraliza excepciones de dominio como `QuotaExceeded`, `SubscriptionInactive` o `OwnershipViolation`. Evita que cada app defina sus propias excepciones incompatibles y facilita el manejo uniforme de errores.

**`apps/common/context_processors.py`**

Las plantillas necesitan conocer los límites del plan activo del usuario para mostrar o bloquear elementos de UI. Un context processor dedicado inyecta esta información en cada request autenticado sin duplicar lógica en las vistas.

**`apps/users/managers.py`**

El custom `UserManager` debe estar desacoplado del modelo para mantener cada fichero con una responsabilidad única. Mezclar manager y modelo en el mismo fichero viola el principio de responsabilidad única y dificulta los tests.

**`apps/users/backends.py`**

Django requiere un backend de autenticación explícito para usar email como identificador en lugar de username. Este fichero implementa `AUTHENTICATION_BACKENDS` y mantiene esa lógica fuera del modelo.

**`apps/users/signals.py`**

La creación automática del perfil de usuario al registrarse debe ocurrir de forma reactiva. Una señal `post_save` en este fichero cumple esa función sin acoplar la lógica de creación de perfil al modelo de usuario.

**`apps/users/tokens.py`**

La verificación de email y el reset de contraseña requieren generadores de tokens seguros y con expiración. Centralizar esto en un fichero dedicado evita dispersar la lógica criptográfica.

**`apps/billing/admin.py`**

El admin de Django debe ser realmente útil para soporte y supervisión, no solo generado por defecto. Los planes y suscripciones son entidades críticas que deben ser gestionables desde el admin con filtros, búsqueda y acciones.

**`apps/billing/selectors.py`**

Las consultas de cuota, límites por plan y estado de suscripción son reutilizadas por `common`, `collections` y `billing`. Centralizar estas consultas en selectors evita duplicación y garantiza que siempre se use la misma lógica de negocio.

**`apps/audit/admin.py`**

Los AuditLog deben ser visualizables por staff desde el admin con filtros por usuario, acción y fecha. Sin este fichero, el admin no registra la app de auditoría y los logs son inaccesibles desde la interfaz de administración.

**`templates/emails/`**

La verificación de email, el reset de contraseña y las alertas de seguridad son requisitos explícitos del dominio. Estas funciones requieren plantillas de correo HTML y texto plano en una ubicación conocida y mantenible.

**`templates/errors/`**

Las páginas de error personalizadas (400, 403, 404, 500) son obligatorias para evitar la filtración involuntaria de información del servidor como rutas internas, versiones de software o trazas de stack. Django las sirve automáticamente si existen en esta ubicación.

## 9. Reglas de diseño por capa

### 9.1 Models

Los modelos deben representar el dominio, sus invariantes y relaciones. No deben convertirse en contenedores caóticos de lógica transversal.

Deben incluir:

- restricciones de base de datos.
- índices útiles.
- validaciones coherentes.
- nombres explícitos.
- timestamps estandarizados.
- soft delete solo si existe necesidad real y diseño consistente.

### 9.2 Forms o serializers

Responsables de validar entrada externa, normalizar datos y devolver errores claros. No deben incorporar reglas de autorización.

### 9.3 Services

Responsables de casos de uso con varias operaciones o reglas de negocio relevantes.

Ejemplos:

- crear colección.
- añadir elemento.
- cambiar plan premium.
- registrar evento de auditoría.

### 9.4 Selectors

Responsables de consultas complejas reutilizables y optimizadas. Útiles para evitar lógica de acceso a datos dispersa en vistas.

### 9.5 Views

Responsables de orquestación HTTP, permisos, formularios y respuesta. Deben ser delgadas.

## 10. Persistencia y base de datos

Base de datos recomendada para producción: PostgreSQL.

Razones:

- mayor solidez.
- mejores índices y constraints.
- mejor soporte para búsquedas, JSON y evolución futura.
- opción estándar seria para Django en producción.

Reglas:

- SQLite puede usarse solo en desarrollo local si simplifica el arranque.
- En staging y producción, PostgreSQL.
- Definir constraints de unicidad, índices e integridad relacional desde migraciones.

## 11. SEO y visibilidad

El SEO no debe comprometer privacidad ni seguridad.

Decisiones:

- Solo contenido público puede indexarse.
- Nada privado de usuarios debe exponerse por error a buscadores.
- URLs limpias y semánticas.
- metadatos bien definidos.
- sitemap y robots coherentes cuando existan páginas públicas.
- canonical tags donde aplique.
- rendimiento y accesibilidad como factores SEO reales.

## 12. Observabilidad y auditoría

Debe existir una base mínima operativa desde el inicio:

- logging estructurado.
- separación entre logs de aplicación, seguridad y auditoría.
- correlación básica por request si es viable.
- monitorización de errores.
- auditoría en acciones críticas.

No se debe registrar:

- contraseñas.
- tokens en claro.
- datos sensibles innecesarios.
- payloads completos si contienen información personal no imprescindible.

## 13. Testing obligatorio

La calidad no es negociable sin pruebas.

Capas mínimas:

- tests de modelos.
- tests de formularios.
- tests de permisos.
- tests de servicios.
- tests de vistas críticas.
- tests de integración para flujos principales.

Flujos mínimos a cubrir:

- registro y login.
- recuperación de acceso.
- creación de colección.
- alta y edición de elemento.
- subida segura de imagen.
- restricción de acceso a recursos ajenos.
- cambio de estado premium.
- registro de auditoría en operaciones sensibles.

## 14. Dependencias y tooling recomendados

Dependencias base razonables para evaluar:

- Django.
- psycopg para PostgreSQL.
- Pillow para imágenes.
- django-environ o equivalentemente python-decouple si se prefiere.
- whitenoise si se sirve estático de forma simple.
- django-axes o solución equivalente para endurecer autenticación.
- django-csp para configurar Content Security Policy de forma estructurada y por entorno.
- pytest, pytest-django y factory_boy para testing.
- ruff y mypy si el equipo adopta tipado progresivo.
- pre-commit para ejecutar linters y formatters automáticamente antes de cada commit.

Regla:

- No añadir paquetes si Django ya resuelve el problema correctamente.

## 15. Roadmap técnico recomendado

### Fase 1

- Crear proyecto base.
- Configurar settings por entorno.
- Implementar custom user.
- Montar autenticación segura.
- Configurar linters, formatters y tests.

### Fase 2

- Implementar colecciones y elementos.
- Implementar subida segura de imágenes.
- Añadir permisos por ownership.
- Añadir admin útil.

### Fase 3

- Implementar roles y suscripción premium.
- Añadir auditoría robusta.
- Añadir páginas públicas si el producto lo requiere.

### Fase 4

- Preparar observabilidad, despliegue y endurecimiento final.
- Revisar rendimiento.
- Revisar cumplimiento legal y privacidad.

## 16. Riesgos y decisiones críticas

- No sobrediseñar facturación antes de tener pasarela real.
- No almacenar más datos personales de los necesarios.
- No mezclar permisos de negocio con hacks de interfaz.
- No asumir que media y contenido privado pueden servirse igual.
- No dejar auditoría para el final.
- No usar el User por defecto si ya sabemos que habrá personalización.

## 17. Definición de éxito

El proyecto estará bien definido cuando cumpla estas condiciones:

- el dominio esté claramente separado en contextos coherentes.
- la seguridad esté integrada en autenticación, autorización, ficheros y operación.
- la estructura Django permita crecer sin rehacer el proyecto.
- las reglas del negocio estén expresadas en modelos, servicios y permisos de forma clara.
- el código pueda mantenerse por un equipo senior sin deuda innecesaria.
- exista una base suficientemente sólida para pasar de MVP serio a producto real.

## 18. Conclusión de diseño

Este proyecto no debe plantearse como una simple web para guardar objetos, sino como una plataforma seria de gestión de colecciones personales con criterios profesionales de ingeniería. La forma correcta de abordarlo en Django es construir primero una base segura, coherente y disciplinada, y después añadir funcionalidades sin comprometer el diseño.

La consigna técnica correcta es esta: menos improvisación, más límites claros, más seguridad, más pruebas y más separación de responsabilidades.

