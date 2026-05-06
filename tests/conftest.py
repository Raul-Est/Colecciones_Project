# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Configuración global de pytest para el proyecto.

El DJANGO_SETTINGS_MODULE ya está definido en pyproject.toml.
Este fichero sirve como punto de extensión para fixtures compartidas
entre todos los módulos de tests.
"""
import pytest


@pytest.fixture
def usuario_anonimo(client):
    """Cliente HTTP sin autenticar."""
    return client
