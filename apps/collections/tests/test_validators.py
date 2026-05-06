# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.
"""
Tests del validador de caratulas (apps/collections/validators.py).
"""

import io
import sys
from unittest.mock import MagicMock, patch

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.collections.validators import _check_nudenet, validate_cover

# -- Helpers ------------------------------------------------------------------

def _make_image_bytes(width=200, height=200, fmt='JPEG'):
    buf = io.BytesIO()
    Image.new('RGB', (width, height), color=(100, 150, 200)).save(buf, format=fmt)
    return buf.getvalue()


def _make_file(width=200, height=200, name='test.jpg', size_override=None):
    content = _make_image_bytes(width, height)
    f = SimpleUploadedFile(name, content, content_type='image/jpeg')
    if size_override is not None:
        f.size = size_override
    return f


# -- Tests de extension -------------------------------------------------------

@pytest.mark.django_db
class TestExtension:

    def test_extension_valida_jpg(self):
        f = _make_file(name='foto.jpg')
        with patch('apps.collections.validators._check_nudenet'):
            validate_cover(f)  # no debe lanzar

    def test_extension_no_permitida(self):
        f = _make_file(name='archivo.gif')
        with pytest.raises(ValidationError, match='no permitida'):
            validate_cover(f)

    def test_extension_ejecutable_rechazada(self):
        f = _make_file(name='malware.exe')
        with pytest.raises(ValidationError, match='no permitida'):
            validate_cover(f)


# -- Tests de MIME ------------------------------------------------------------

class TestMime:

    def test_mime_falso_rechazado(self):
        f = SimpleUploadedFile('trampa.jpg', b'esto no es una imagen', content_type='image/jpeg')
        with pytest.raises(ValidationError, match='tipo MIME no reconocido'):
            validate_cover(f)


# -- Tests de tamanyo ---------------------------------------------------------

class TestSize:

    def test_tamanyo_maximo_superado(self):
        f = _make_file(size_override=6 * 1024 * 1024)
        with pytest.raises(ValidationError, match='5 MB'):
            validate_cover(f)

    def test_tamanyo_en_limite_pasa(self):
        f = _make_file(size_override=5 * 1024 * 1024)
        with patch('apps.collections.validators._check_nudenet'):
            validate_cover(f)  # no debe lanzar


# -- Tests de dimensiones -----------------------------------------------------

class TestDimensions:

    def test_imagen_demasiado_pequena(self):
        f = _make_file(width=50, height=50)
        with pytest.raises(ValidationError, match='demasiado'):
            validate_cover(f)

    def test_imagen_demasiado_grande(self):
        f = _make_file(width=5000, height=5000)
        with pytest.raises(ValidationError, match='grande'):
            validate_cover(f)

    def test_dimensiones_validas(self):
        f = _make_file(width=300, height=400)
        with patch('apps.collections.validators._check_nudenet'):
            validate_cover(f)  # no debe lanzar


# -- Tests de NudeNet ---------------------------------------------------------
# NudeDetector se importa localmente dentro de _check_nudenet con:
#   from nudenet import NudeDetector
# El patch correcto es sobre sys.modules['nudenet'], no sobre el modulo validators.

class TestNudeNet:

    def test_contenido_explicito_rechazado(self):
        f = _make_file()
        mock_detector = MagicMock()
        mock_detector.detect.return_value = [
            {'class': 'FEMALE_BREAST_EXPOSED', 'score': 0.95}
        ]
        mock_nudenet = MagicMock()
        mock_nudenet.NudeDetector.return_value = mock_detector
        with patch.dict(sys.modules, {'nudenet': mock_nudenet}):
            with pytest.raises(ValidationError, match='inapropiado'):
                _check_nudenet(f)

    def test_sin_detecciones_pasa(self):
        f = _make_file()
        mock_detector = MagicMock()
        mock_detector.detect.return_value = []
        mock_nudenet = MagicMock()
        mock_nudenet.NudeDetector.return_value = mock_detector
        with patch.dict(sys.modules, {'nudenet': mock_nudenet}):
            _check_nudenet(f)  # no debe lanzar

    def test_deteccion_bajo_umbral_pasa(self):
        f = _make_file()
        mock_detector = MagicMock()
        mock_detector.detect.return_value = [
            {'class': 'FEMALE_BREAST_EXPOSED', 'score': 0.3}
        ]
        mock_nudenet = MagicMock()
        mock_nudenet.NudeDetector.return_value = mock_detector
        with patch.dict(sys.modules, {'nudenet': mock_nudenet}):
            _check_nudenet(f)  # no debe lanzar

    def test_nudenet_no_instalado_no_bloquea(self):
        f = _make_file()
        with patch.dict(sys.modules, {'nudenet': None}):
            _check_nudenet(f)  # no debe lanzar
