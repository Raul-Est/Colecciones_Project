# Copyright (c) 2026 Raúl Esteban Posadilla. Todos los derechos reservados.
# Software privativo. Uso no autorizado expresamente prohibido.

import tempfile
import uuid
from pathlib import Path

from django.core.exceptions import ValidationError
from PIL import Image

# ── Constantes ────────────────────────────────────────────────────────────────

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_MIME_BYTES = {
    b'\xff\xd8\xff': 'image/jpeg',
    b'\x89PNG': 'image/png',
    b'RIFF': 'image/webp',  # RIFF....WEBP
}
MAX_SIZE_BYTES = 5 * 1024 * 1024          # 5 MB
MIN_DIMENSION = 100                        # px
MAX_DIMENSION = 4000                       # px

# Umbral NudeNet: probabilidad mínima para rechazar la imagen
NUDENET_THRESHOLD = 0.6
NUDENET_UNSAFE_LABELS = {
    'FEMALE_BREAST_EXPOSED',
    'FEMALE_GENITALIA_EXPOSED',
    'MALE_GENITALIA_EXPOSED',
    'BUTTOCKS_EXPOSED',
    'ANUS_EXPOSED',
}


# ── Helpers internos ──────────────────────────────────────────────────────────

def _check_extension(name: str) -> None:
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f'Extensión no permitida: {ext}. Usa jpg, png o webp.'
        )


def _check_mime(data: bytes) -> None:
    """Lee los primeros bytes del fichero y valida el tipo real."""
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return  # WebP válido
    for magic in ALLOWED_MIME_BYTES:
        if magic == b'RIFF':
            continue
        if data[:len(magic)] == magic:
            return
    raise ValidationError(
        'El archivo no es una imagen válida (tipo MIME no reconocido).'
    )


def _check_size(size: int) -> None:
    if size > MAX_SIZE_BYTES:
        mb = size / (1024 * 1024)
        raise ValidationError(
            f'La imagen ocupa {mb:.1f} MB. El límite es 5 MB.'
        )


def _check_dimensions(image: Image.Image) -> None:
    w, h = image.size
    if w < MIN_DIMENSION or h < MIN_DIMENSION:
        raise ValidationError(
            f'La imagen es demasiado pequeña ({w}×{h} px). '
            f'Mínimo: {MIN_DIMENSION}×{MIN_DIMENSION} px.'
        )
    if w > MAX_DIMENSION or h > MAX_DIMENSION:
        raise ValidationError(
            f'La imagen es demasiado grande ({w}×{h} px). '
            f'Máximo: {MAX_DIMENSION}×{MAX_DIMENSION} px.'
        )


def _check_nudenet(uploaded_file) -> None:
    """
    Pasa la imagen por NudeNet. Si detecta contenido explícito por encima
    del umbral, lanza ValidationError. El clasificador es local: ningún
    dato sale del servidor.
    """
    try:
        from nudenet import NudeDetector
    except ImportError:
        return  # Si no está instalado (p.ej. entorno CI), se omite.

    detector = NudeDetector()
    uploaded_file.seek(0)
    suffix = f'_nudenet_{uuid.uuid4().hex}.jpg'
    tmp_fd, tmp_name = tempfile.mkstemp(suffix=suffix)
    tmp_path = Path(tmp_name)
    try:
        import os
        os.close(tmp_fd)
        tmp_path.write_bytes(uploaded_file.read())
        detections = detector.detect(str(tmp_path))
        for det in detections:
            label = det.get('class', '')
            score = det.get('score', 0)
            if label in NUDENET_UNSAFE_LABELS and score >= NUDENET_THRESHOLD:
                raise ValidationError(
                    'La imagen contiene contenido inapropiado y no puede subirse.'
                )
    finally:
        uploaded_file.seek(0)
        if tmp_path.exists():
            tmp_path.unlink()


# ── Función pública ───────────────────────────────────────────────────────────

def validate_cover(uploaded_file) -> None:
    """
    Validador completo para el campo cover de CollectionItem.

    Orden:
      1. Extensión permitida
      2. Tipo MIME real (cabecera de bytes)
      3. Tamaño máximo 5 MB
      4. Dimensiones con Pillow
      5. Contenido inapropiado con NudeNet
    """
    _check_extension(uploaded_file.name)

    uploaded_file.seek(0)
    header = uploaded_file.read(12)
    uploaded_file.seek(0)
    _check_mime(header)

    _check_size(uploaded_file.size)

    uploaded_file.seek(0)
    try:
        image = Image.open(uploaded_file)
        image.load()  # carga completa: detecta ficheros corruptos o truncados
    except ValidationError:
        raise
    except Exception as err:
        raise ValidationError('El archivo no es una imagen válida o está corrupto.') from err
    finally:
        uploaded_file.seek(0)

    _check_dimensions(image)
    uploaded_file.seek(0)

    _check_nudenet(uploaded_file)


# ── Generador de nombre seguro ────────────────────────────────────────────────

def rename_cover(instance, filename: str) -> str:
    """
    Genera una ruta no predecible para el fichero subido.
    El nombre original nunca llega al disco.
    Ejemplo: covers/a3f1bc92-4e7d-4c2a-91ef-3d8f2b1a0c56.jpg
    """
    ext = Path(filename).suffix.lower()
    return f'covers/{uuid.uuid4()}{ext}'
