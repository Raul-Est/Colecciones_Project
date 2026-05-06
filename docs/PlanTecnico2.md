# Plan Tecnico 2. Premium, Endurecimiento y Salida

## 1. Como usar este documento

Este documento es la segunda mitad del manual de montaje del proyecto. Solo se empieza cuando PlanTecnico1.md esta ejecutado hasta Beta 2. La numeracion de pasos continua para mantener un recorrido unico de principio a fin.

El modelo de datos exacto recomendado para planes, suscripciones, limites y estado excedido se detalla en ModeloDatosPlanesSuscripciones.md.

## 2. Punto de entrada a esta segunda mitad

No se debe empezar este documento si aun no se ha validado Beta 2. A partir de aqui se implementan la capa comercial, la trazabilidad seria, la parte publica y la preparacion de salida.

## 3. Bloque E. Premium, planes y administracion operativa

Este bloque mete logica de negocio comercial y administracion seria.

### Paso 42. Modelar plan y suscripcion

Accion:

1. crear la entidad de plan;
2. crear la entidad de suscripcion o equivalente;
3. relacionarlas con el usuario;
4. definir estados como activa, suspendida, vencida y cancelada.

Resultado esperado:

- el sistema ya puede distinguir negocio gratuito y premium con estados claros.

### Paso 43. Modelar capacidades y limites por plan

Accion:

1. definir que privilegios son premium;
2. definir que limites tiene free;
3. definir que limites tiene premium;
4. modelar capacidades de forma explicita y no dispersa en la interfaz.

Resultado esperado:

- las reglas de capacidad dejan de ser ambiguas y pasan a formar parte del dominio.

### Paso 44. Implementar suspension por impago sin perdida de datos

Accion:

1. suspender privilegios premium cuando haya impago;
2. conservar colecciones, elementos, imagenes e historial del usuario;
3. impedir que la suspension provoque borrado fisico o logico automatico;
4. dejar auditado el cambio de estado.

Resultado esperado:

- una cuenta suspendida pierde privilegios premium, pero no pierde propiedad ni contenido.

### Paso 45. Implementar reactivacion automatica de privilegios premium

Accion:

1. detectar regularizacion del pago;
2. devolver la suscripcion a estado activa;
3. reactivar privilegios premium compatibles con el plan;
4. evitar procesos manuales para restaurar acceso a capacidades ya pagadas.

Resultado esperado:

- el usuario recupera su situacion premium sin reconstruir datos ni pedir soporte para ello.

### Paso 46. Implementar downgrade de premium a free sin borrar contenido

Accion:

1. retirar privilegios premium al pasar a free;
2. mantener los datos existentes del usuario;
3. impedir nuevas ampliaciones incompatibles con los limites free;
4. conservar acceso de consulta a los datos ya creados, salvo restriccion funcional muy justificada.

Resultado esperado:

- el usuario no pierde informacion por bajar de plan, pero queda sujeto a los limites reales de free.

### Paso 47. Gestionar el estado excedido respecto al plan free

Accion:

1. detectar cuando un usuario free supera limite de colecciones, elementos, almacenamiento u otras capacidades;
2. bloquear nuevas altas incompatibles con free;
3. comunicar claramente por que esta bloqueado;
4. ofrecer las dos salidas reales: reducir uso o reactivar premium.

Resultado esperado:

- el sistema aplica limites sin borrar contenido y sin comportamientos arbitrarios.

### Paso 48. Implementar vistas de cuenta, plan y estado de limites

Accion:

1. mostrar plan actual;
2. mostrar estado de suscripcion;
3. mostrar limites consumidos;
4. mostrar si el usuario esta suspendido o excedido.

Resultado esperado:

- el usuario entiende su situacion funcional y comercial dentro del producto.

### Paso 49. Endurecer permisos administrativos

Accion:

1. revisar staff;
2. definir permisos granulares;
3. evitar admins todopoderosos sin necesidad;
4. separar acciones de soporte de acciones de alto riesgo.

Resultado esperado:

- la operacion interna es mas segura y controlada.

### Paso 50. Mejorar admin operativo

Accion:

1. filtros utiles;
2. busquedas;
3. acciones seguras;
4. trazabilidad de operaciones administrativas;
5. visibilidad del estado premium, suspendido o excedido.

Resultado esperado:

- el panel de administracion sirve para operar el producto de verdad.

### Paso 51. Probar el Bloque E

Accion:

1. tests de reglas premium;
2. tests de suspension por impago;
3. tests de reactivacion;
4. tests de downgrade a free;
5. tests de estado excedido;
6. tests de permisos por rol y por plan.

Resultado esperado:

- la capa comercial y operativa esta controlada y no depende de supuestos.

### Paso 52. Cerrar el Bloque E

Checklist de cierre:

1. existe plan y suscripcion modelados;
2. existen limites por plan;
3. la suspension no borra datos;
4. la reactivacion restaura privilegios;
5. el downgrade a free no borra contenido;
6. el estado excedido esta controlado;
7. las pruebas del bloque estan en verde.

## 4. Bloque F. Auditoria y endurecimiento serio

Este bloque hace que el sistema ya no solo funcione, sino que sea defendible.

### Paso 53. Crear o completar la app de auditoria

Accion:

1. definir el modelo de auditoria;
2. definir eventos minimos;
3. decidir que metadatos se guardan y cuales no.

Resultado esperado:

- existe una base formal para trazabilidad.

### Paso 54. Auditar eventos criticos

Accion:

1. accesos;
2. cambios de credenciales;
3. cambios administrativos;
4. cambios de suscripcion;
5. suspensiones por impago;
6. reactivaciones;
7. downgrades y estados excedidos;
8. eliminaciones o restauraciones sensibles.

Resultado esperado:

- los eventos importantes dejan rastro.

### Paso 55. Revisar logs y monitorizacion

Accion:

1. revisar logging estructurado;
2. preparar monitorizacion de errores;
3. asegurar que no se registran secretos.

Resultado esperado:

- se mejora la capacidad de soporte y diagnostico.

### Paso 56. Ejecutar revision completa de permisos

Accion:

1. revisar usuarios normales;
2. revisar premium;
3. revisar suspendidos por impago;
4. revisar usuarios free excedidos;
5. revisar staff;
6. revisar admin;
7. revisar ownership en todos los recursos.

Resultado esperado:

- disminuye el riesgo de fuga o abuso por autorizacion defectuosa.

### Paso 57. Probar el Bloque F

Accion:

1. tests de auditoria;
2. tests de regresion de permisos;
3. tests de escenarios sensibles.

Resultado esperado:

- la trazabilidad y el endurecimiento no dependen de confianza manual.

### Paso 58. Cerrar el Bloque F

Checklist de cierre:

1. existe auditoria funcional;
2. los eventos criticos quedan registrados;
3. los permisos se han revisado;
4. las pruebas del bloque estan en verde.

## 5. Beta 3. Beta avanzada de negocio

La Beta 3 se prepara solo cuando los Bloques E y F estan cerrados.

### Que debe poder demostrarse

1. flujo completo del usuario autenticado;
2. diferenciacion free y premium;
3. suspension por impago sin perdida de datos;
4. downgrade a free con conservacion de contenido;
5. administracion interna;
6. trazabilidad;
7. sensacion de producto serio y no de prototipo.

### Objetivo de la Beta 3

Validar que el producto ya cubre la propuesta de valor central y decidir que falta antes de salida controlada.

## 6. Bloque G. SEO, contenido publico y calidad final

Este bloque solo se toca cuando la privacidad ya esta bien defendida.

### Paso 59. Definir que puede ser publico

Accion:

1. decidir que colecciones o vistas pueden exponerse;
2. documentar que nunca sera publico;
3. alinear esto con negocio y privacidad.

Resultado esperado:

- el producto sabe claramente que puede enseñar fuera del area privada.

### Paso 60. Implementar visibilidad publica controlada

Accion:

1. exponer solo contenido autorizado;
2. aplicar reglas claras de visibilidad;
3. impedir indexacion de contenido privado.

Resultado esperado:

- lo publico no compromete la privacidad.

### Paso 61. Añadir SEO tecnico basico

Accion:

1. urls limpias;
2. metadatos;
3. sitemap si aplica;
4. robots si aplica;
5. canonical cuando corresponda.

Resultado esperado:

- existe base SEO sin hacer barbaridades de privacidad.

### Paso 62. Mejorar accesibilidad y rendimiento

Accion:

1. revisar plantillas;
2. revisar estructura semantica;
3. revisar tiempos de carga basicos;
4. revisar experiencia movil.

Resultado esperado:

- mejora la calidad final y la sensacion de producto maduro.

### Paso 63. Probar el Bloque G

Accion:

1. tests de visibilidad publica;
2. tests de privacidad;
3. comprobaciones funcionales del contenido indexable.

Resultado esperado:

- la capa publica no rompe el modelo de seguridad.

### Paso 64. Cerrar el Bloque G

Checklist de cierre:

1. lo publico esta definido;
2. lo privado no se indexa;
3. existe SEO basico correcto;
4. las pruebas del bloque estan en verde.

## 7. Bloque H. Preproduccion y salida controlada

Este bloque prepara el producto para una beta final muy estable o un despliegue controlado.

### Paso 65. Preparar configuracion de production

Accion:

1. revisar settings de production;
2. revisar secretos;
3. revisar servicios externos necesarios.

Resultado esperado:

- el proyecto esta listo para salir de entorno de desarrollo.

### Paso 66. Endurecer seguridad final

Accion:

1. HSTS;
2. secure cookies;
3. cabeceras seguras;
4. cuentas internas revisadas;
5. dependencias revisadas.

Resultado esperado:

- el entorno productivo esta mas endurecido.

### Paso 67. Preparar despliegue reproducible

Accion:

1. definir flujo de despliegue;
2. preparar checklist;
3. revisar migraciones;
4. revisar rollback basico si aplica.

Resultado esperado:

- el paso a entorno real no depende de improvisacion.

### Paso 68. Revisar backup, restauracion y operacion

Accion:

1. revisar backup;
2. revisar restauracion;
3. revisar logs y alertas;
4. revisar soporte operativo minimo.

Resultado esperado:

- el sistema ya no solo se despliega, tambien puede mantenerse.

### Paso 69. Ejecutar bateria final de pruebas

Accion:

1. tests completos;
2. revision manual del flujo critico;
3. verificacion de permisos;
4. verificacion de demo final.

Resultado esperado:

- se reduce el riesgo de llegar rotos a la presentacion final o a produccion.

### Paso 70. Cerrar documentacion tecnica y operativa

Accion:

1. actualizar README;
2. documentar despliegue;
3. documentar operacion;
4. documentar incidencias habituales.

Resultado esperado:

- el proyecto puede mantenerse sin depender de memoria informal.

### Paso 71. Cerrar el Bloque H

Checklist de cierre:

1. produccion esta preparada;
2. la seguridad final esta revisada;
3. el despliegue es reproducible;
4. la documentacion existe;
5. las pruebas finales estan cerradas.

## 8. Beta final o release candidate

La beta final se prepara solo cuando los Bloques G y H estan cerrados.

### Que debe poder demostrarse

1. producto casi completo;
2. experiencia principal cerrada;
3. administracion madura;
4. seguridad coherente;
5. capacidad real de despliegue.

### Objetivo de la beta final

Cerrar ajustes menores y decidir salida a produccion o piloto controlado.

## 9. Resumen de orden exacto de esta segunda mitad

El orden que debe seguirse sin saltos desde Beta 2 es este:

1. Bloque E completo.
2. Bloque F completo.
3. Beta 3.
4. Bloque G completo.
5. Bloque H completo.
6. Beta final.

## 10. Tareas que nunca se abandonan durante todo el plan

Estas tareas siguen vivas tambien en esta segunda mitad:

1. mantener tests al dia;
2. revisar seguridad en cada funcionalidad nueva;
3. revisar migraciones antes de integrarlas;
4. mantener documentacion viva;
5. revisar dependencias y vulnerabilidades;
6. preparar demo interna antes de cada beta cliente.

## 11. Criterio real de beta enseñable

Una beta solo se enseña al cliente si cumple estas condiciones:

1. el flujo principal de la beta funciona de verdad;
2. no hay errores graves conocidos en la demo;
3. la seguridad del bloque demostrado esta razonablemente cerrada;
4. la interfaz transmite orden, aunque aun no este finalizada;
5. se puede explicar claramente que esta hecho y que vendra despues.