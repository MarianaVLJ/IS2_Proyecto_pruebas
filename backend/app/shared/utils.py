import os
from werkzeug.utils import secure_filename
from app.config.settings import settings
from uuid import uuid4


def guardar_evidencia(file):
    if not file:
        return None, "Archivo vacio"

    filename = secure_filename(file.filename)
    ext = filename.rsplit('.', 1)[-1].lower()

    if ext not in settings.ALLOWED_EXTENSIONS:
        return None, f"Extension '{ext}' no permitida"

    os.makedirs(settings.UPLOADS_FOLDER, exist_ok=True)

    unique_name = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(settings.UPLOADS_FOLDER, unique_name)
    file.save(file_path)

    return unique_name, None
