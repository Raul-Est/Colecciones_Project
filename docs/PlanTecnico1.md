# Plan Tecnico 1. Base, Identidad y Beta Funcional

## 1. Como usar este documento

Este documento es la primera mitad del manual de montaje del proyecto. Se ejecuta de arriba a abajo y se detiene en Beta 2. La segunda mitad continua en PlanTecnico2.md.

La ejecucion operativa detallada de esta primera mitad se desarrolla en ImplementacionPlanTecnico1.md.

La regla principal es esta:

1. ejecutar el siguiente paso;
2. comprobar que el resultado esperado existe de verdad;
3. no continuar si el paso anterior no esta cerrado;
4. al llegar a un hito beta, preparar demo interna y luego demo cliente.

## 2. Reglas del manual

Antes de pasar de un paso al siguiente, deben cumplirse estas condiciones:

1. el codigo arranca;
2. no se rompe lo ya construido;
3. hay validacion minima de tests o comprobacion funcional;
4. la seguridad de ese bloque esta aplicada;
5. la documentacion minima esta actualizada.

Regla operativa:

1. no abrir varios frentes si uno no esta cerrado;
2. no dejar seguridad para despues;
3. no avanzar por interfaz si el backend aun no esta bien definido;
4. no enseñar al cliente nada que no aguante una demo de verdad.

## 3. Bloque A. Base segura del proyecto

Este bloque construye el armazon tecnico del proyecto. Sin esto, todo lo demas nace mal.

### Paso 1. Crear la estructura raiz del proyecto

Accion:

1. crear la carpeta del proyecto Django;
2. definir la estructura raiz con config, apps, templates, static, media, tests y requirements o equivalente;
3. dejar decidido desde el inicio que habra settings separados por entorno.

Resultado esperado:

- existe una estructura ordenada y estable;
- cualquier desarrollador entiende donde va cada pieza.

### Paso 2. Inicializar el proyecto Django

Accion:

1. crear el proyecto principal;
2. colocar config como contenedor de urls, asgi, wsgi y settings;
3. comprobar que el proyecto arranca.

Resultado esperado:

- el proyecto ejecuta el servidor sin errores;
- la base tecnica ya existe.

### Paso 3. Separar configuracion por entornos

Accion:

1. crear base.py;
2. crear local.py;
3. crear test.py;
4. crear production.py;
5. dejar claro como se selecciona cada entorno.

Resultado esperado:

- la configuracion no esta mezclada;
- el proyecto ya esta preparado para crecer sin caos.

### Paso 4. Preparar variables de entorno y secretos

Accion:

1. crear un archivo de ejemplo para variables de entorno;
2. sacar fuera del codigo los secretos;
3. documentar variables obligatorias.

Resultado esperado:

- no hay secretos en el repositorio;
- el equipo sabe que necesita para arrancar.

### Paso 5. Configurar dependencias del proyecto

Accion:

1. definir dependencias base;
2. separar dependencias por entorno si se necesita;
3. fijar herramientas de calidad como formatter, linter y testing.

Resultado esperado:

- las dependencias estan organizadas;
- el proyecto puede instalarse de forma consistente.

### Paso 6. Configurar base de datos con objetivo PostgreSQL

Accion:

1. dejar PostgreSQL como base objetivo;
2. permitir SQLite solo para local si simplifica el arranque inicial;
3. documentar claramente esta decision.

Resultado esperado:

- la persistencia esta planteada correctamente desde el inicio.

### Paso 7. Configurar seguridad minima obligatoria

Accion:

1. preparar ALLOWED_HOSTS por entorno;
2. desactivar DEBUG en production;
3. activar CSRF y X-Frame-Options;
4. dejar preparadas cookies seguras, HttpOnly y SameSite;
5. preparar cabeceras seguras para produccion.

Resultado esperado:

- la seguridad base no queda aplazada;
- el proyecto nace con una postura correcta.

### Paso 8. Configurar logging y observabilidad minima

Accion:

1. definir logging base;
2. separar como minimo logs de aplicacion y errores;
3. dejar preparado el camino para auditoria posterior.

Resultado esperado:

- los errores ya no son invisibles;
- existe base para soporte real.

### Paso 9. Preparar static, media y plantilla base

Accion:

1. configurar static;
2. configurar media;
3. crear una plantilla base reutilizable;
4. dejar un layout inicial sobrio y limpio.

Resultado esperado:

- el proyecto ya puede servir interfaz y recursos de forma ordenada.

### Paso 10. Configurar calidad automatica

Accion:

1. configurar formatter;
2. configurar linter;
3. configurar pytest;
4. preparar una cobertura minima razonable.

Resultado esperado:

- el proyecto tiene disciplina tecnica desde el inicio.

### Paso 11. Escribir el README tecnico inicial

Accion:

1. documentar arranque local;
2. documentar variables necesarias;
3. documentar comandos base;
4. documentar estructura general.

Resultado esperado:

- otra persona puede entrar al proyecto sin depender de explicacion oral.

### Paso 12. Cerrar el Bloque A

Checklist de cierre:

1. el proyecto arranca;
2. existe separacion por entorno;
3. no hay secretos en codigo;
4. los linters y tests se pueden ejecutar;
5. la documentacion inicial existe.

## 4. Bloque B. Usuarios, identidad y autenticacion

Este bloque crea la primera pieza de negocio real. Aqui se define la identidad del sistema y no debe improvisarse.

### Paso 13. Crear el modelo de usuario personalizado

Accion:

1. crear custom user model;
2. usar email como identificador principal;
3. definir manager para usuario y superusuario;
4. conectar AUTH_USER_MODEL desde el inicio.

Resultado esperado:

- la base de identidad esta bien planteada;
- no habra que rehacer usuarios mas adelante.

### Paso 14. Crear perfil de usuario desacoplado

Accion:

1. separar autenticacion de datos de perfil;
2. dejar el perfil con campos realmente necesarios;
3. evitar meter datos sensibles sin necesidad real.

Resultado esperado:

- el diseño de usuario queda limpio y ampliable.

### Paso 15. Implementar registro de usuario

Accion:

1. crear formulario y vista de registro;
2. validar datos en backend;
3. controlar mensajes de error sin filtrar informacion sensible.

Resultado esperado:

- un nuevo usuario puede darse de alta de forma segura.

### Paso 16. Implementar login y logout

Accion:

1. crear flujo de login;
2. crear flujo de logout;
3. proteger la sesion correctamente.

Resultado esperado:

- el acceso al sistema funciona de forma segura y clara.

### Paso 17. Implementar cambio y recuperacion de contraseña

Accion:

1. activar cambio de contraseña para usuario autenticado;
2. activar recuperacion para usuario no autenticado;
3. definir mensajes y flujo consistentes.

Resultado esperado:

- existe un ciclo de acceso serio y completo.

### Paso 18. Endurecer autenticacion

Accion:

1. aplicar rate limiting al login;
2. aplicar rate limiting a recuperacion de contraseña;
3. definir politica minima de contraseñas;
4. preparar verificacion de email si entra en alcance temprano.

Resultado esperado:

- la autenticacion no queda expuesta de forma ingenua.

### Paso 19. Definir grupos y permisos base

Accion:

1. crear grupos free, premium y staff;
2. definir permisos iniciales;
3. decidir que se controla por permiso y que por rol.

Resultado esperado:

- el sistema tiene una primera base de autorizacion coherente.

### Paso 20. Preparar admin de usuarios y perfiles

Accion:

1. configurar Django admin para usuarios;
2. exponer datos utiles para soporte;
3. evitar mostrar informacion sensible innecesaria.

Resultado esperado:

- existe backoffice basico util desde pronto.

### Paso 21. Crear auditoria basica de eventos de acceso

Accion:

1. registrar inicios de sesion;
2. registrar intentos fallidos relevantes si se decide incluirlos ya;
3. registrar cambios sensibles de credenciales.

Resultado esperado:

- ya existe trazabilidad basica sobre identidad.

### Paso 22. Probar todo el Bloque B

Accion:

1. crear tests de modelo de usuario;
2. crear tests de registro;
3. crear tests de login y logout;
4. crear tests de permisos base;
5. crear tests de sesiones y seguridad minima.

Resultado esperado:

- la base de identidad esta defendida por pruebas.

### Paso 23. Cerrar el Bloque B

Checklist de cierre:

1. el usuario puede registrarse;
2. puede iniciar y cerrar sesion;
3. puede recuperar acceso;
4. existe admin basico;
5. existen permisos base;
6. existe auditoria basica;
7. los tests del bloque estan en verde.

## 5. Beta 1. Primera demo cliente

La Beta 1 se prepara solo cuando los Bloques A y B estan cerrados.

### Que debe poder demostrarse

1. acceso al sistema;
2. pantalla de login;
3. registro de usuario si aplica;
4. sesion segura;
5. perfil basico;
6. estructura profesional de producto ya arrancado.

### Objetivo de la Beta 1

Demostrar que ya existe una base real, segura y seria. Aqui el cliente no debe ver una maqueta: debe ver un producto empezando bien.

### Condicion para pasar al siguiente bloque

No se pasa al siguiente bloque sin demo interna estable de Beta 1.

## 6. Bloque C. Colecciones y elementos

Este bloque construye el corazon del producto.

### Paso 24. Crear el modelo Collection

Accion:

1. crear el modelo de coleccion;
2. asociarlo al propietario;
3. definir nombre, descripcion, visibilidad y slug;
4. añadir restricciones adecuadas.

Resultado esperado:

- ya existe la entidad principal de negocio.

### Paso 25. Crear el modelo CollectionItem

Accion:

1. crear el modelo de elemento;
2. asociarlo a una coleccion;
3. definir campos de descripcion y comentario personal;
4. definir orden, estado y timestamps.

Resultado esperado:

- ya existe la unidad coleccionable del sistema.

### Paso 26. Crear migraciones y constraints correctos

Accion:

1. definir unicidad por propietario donde corresponda;
2. revisar integridad relacional;
3. aplicar indices utiles.

Resultado esperado:

- la base de datos protege el dominio y no solo el codigo.

### Paso 27. Implementar formularios de colecciones

Accion:

1. crear formularios de alta y edicion;
2. validar todo en backend;
3. no permitir asignar propietario desde el cliente.

Resultado esperado:

- la entrada de datos esta controlada correctamente.

### Paso 28. Implementar vistas CRUD de colecciones

Accion:

1. listado;
2. detalle;
3. creacion;
4. edicion;
5. borrado.

Resultado esperado:

- el usuario ya puede operar con sus colecciones.

### Paso 29. Implementar vistas CRUD de elementos

Accion:

1. alta de elemento;
2. edicion de elemento;
3. detalle si aplica;
4. borrado;
5. integracion con la navegacion de colecciones.

Resultado esperado:

- el flujo principal de producto ya esta vivo.

### Paso 30. Aplicar ownership estricto

Accion:

1. filtrar todos los recursos por propietario;
2. impedir acceso a objetos ajenos;
3. revisar vistas, servicios y admin.

Resultado esperado:

- no hay cruce de datos entre usuarios.

### Paso 31. Crear selectors y servicios donde hagan falta

Accion:

1. mover consultas reutilizables a selectors;
2. mover logica de negocio no trivial a services;
3. mantener las vistas delgadas.

Resultado esperado:

- el codigo escala sin degradarse rapido.

### Paso 32. Mejorar admin de colecciones y elementos

Accion:

1. añadir listados utiles;
2. añadir filtros;
3. añadir busquedas;
4. revisar permisos en admin.

Resultado esperado:

- existe soporte operativo tambien para el nucleo del producto.

### Paso 33. Probar el Bloque C

Accion:

1. tests de modelos;
2. tests de formularios;
3. tests de permisos;
4. tests de ownership;
5. tests de vistas principales.

Resultado esperado:

- el corazon funcional esta cubierto por pruebas.

### Paso 34. Cerrar el Bloque C

Checklist de cierre:

1. el usuario crea colecciones;
2. el usuario crea elementos;
3. solo ve y modifica lo suyo;
4. el admin basico funciona;
5. las pruebas del bloque estan en verde.

## 7. Bloque D. Caratulas, imagenes y experiencia visual

Este bloque hace que el producto empiece a parecer un producto y no solo un CRUD correcto.

### Paso 35. Crear el modelo de imagen o caratula

Accion:

1. definir relacion con el elemento;
2. almacenar archivo y metadatos relevantes;
3. contemplar origen de la imagen.

Resultado esperado:

- la imagen ya es una entidad controlada del sistema.

### Paso 36. Implementar subida segura de imagenes

Accion:

1. validar tipo real;
2. validar tamano;
3. validar dimensiones;
4. renombrar archivo de forma no predecible;
5. reprocesar si hace falta.

Resultado esperado:

- la subida de media no abre un agujero de seguridad obvio.

### Paso 37. Asociar caratulas a elementos

Accion:

1. permitir subida desde formulario;
2. vincular la imagen al elemento correcto;
3. impedir asociaciones ajenas o manipuladas.

Resultado esperado:

- cada elemento puede mostrarse con apoyo visual real.

### Paso 38. Mejorar la interfaz de listados y detalle

Accion:

1. mejorar vistas de colecciones;
2. mejorar vistas de elementos;
3. mostrar imagenes;
4. mantener claridad y sobriedad.

Resultado esperado:

- el producto ya es demostrable con mejor impacto visual.

### Paso 39. Añadir accesibilidad minima y texto alternativo

Accion:

1. incluir alt text;
2. revisar estructura semantica;
3. evitar una interfaz vistosa pero poco usable.

Resultado esperado:

- mejora la calidad percibida y la base SEO futura.

### Paso 40. Probar el Bloque D

Accion:

1. tests de subida segura;
2. tests de permisos sobre imagenes;
3. tests de integracion del flujo visual principal.

Resultado esperado:

- las caratulas no son un adorno fragil, sino una funcionalidad seria.

### Paso 41. Cerrar el Bloque D

Checklist de cierre:

1. hay imagenes en elementos;
2. la subida es segura;
3. la interfaz ya es enseñable;
4. las pruebas del bloque estan en verde.

## 8. Beta 2. Producto ya utilizable

La Beta 2 se prepara solo cuando los Bloques C y D estan cerrados.

### Que debe poder demostrarse

1. registro y login;
2. perfil basico;
3. creacion de colecciones;
4. creacion y edicion de elementos;
5. subida de caratulas;
6. navegacion coherente;
7. primera experiencia cercana al producto real.

### Objetivo de la Beta 2

Demostrar que la idea principal ya funciona y que el cliente puede reconocer claramente el valor del producto.

### Feedback que hay que pedir al cliente

1. que tipos de coleccion prioriza;
2. que campos faltan o sobran;
3. que sensacion le transmite la experiencia;
4. si el enfoque visual va en buena direccion.

## 9. Paso siguiente

Cuando Beta 2 este validada, la continuacion exacta del trabajo sigue en PlanTecnico2.md, empezando por el modelado de planes, premium, suspension por impago, downgrade a free sin perdida de datos y reactivacion de privilegios.