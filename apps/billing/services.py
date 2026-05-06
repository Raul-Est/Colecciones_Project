# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

from .models import Subscription


def user_can_use_groups(user) -> bool:
    """
    Devuelve True si el usuario tiene permiso para crear grupos en colecciones.

    Reglas:
    - Los usuarios staff siempre tienen acceso.
    - El resto necesita una suscripción activa cuyo plan tenga can_use_groups=True.
    - Un usuario free (sin suscripción activa premium) recibe False.
    """
    if user.is_staff:
        return True
    return Subscription.objects.filter(
        user=user,
        status=Subscription.Status.ACTIVE,
        plan__can_use_groups=True,
    ).exists()
