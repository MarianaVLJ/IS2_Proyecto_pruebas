from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.infrastructure.database.user_document import UserDocument
from app.infrastructure.database.reaccion_repo_impl import (
    MongoReaccionRepository
)
from app.infrastructure.database.publicacion_repo_impl import (
    MongoPublicacionRepository
)
from app.application.use_cases.crear_publicacion import CrearPublicacionUseCase
from app.application.use_cases.obtener_publicaciones import (
    ObtenerPublicacionesUseCase
)
from app.application.use_cases.editar_publicacion import (
    EditarPublicacionUseCase
)
from app.application.use_cases.eliminar_publicacion import (
    EliminarPublicacionUseCase
)
from app.application.use_cases.reaccionar_publicacion import (
    ReaccionarPublicacionUseCase
)
from app.application.use_cases.eliminar_reaccion import (
    EliminarReaccionUseCase
)

# Constantes - Solución al issue de SonarQube
ERROR_USUARIO_NO_ENCONTRADO = "Usuario no encontrado"
ERROR_CONTENIDO_VACIO = "El contenido no puede estar vacío"
ERROR_SIN_PERMISOS_EDITAR = "No tienes permisos para editar esta publicación"
ERROR_SIN_PERMISOS_ELIMINAR = "No tienes permisos para eliminar esta publicación"
ERROR_YA_REACCIONADO = "Ya has reaccionado a esta publicación"
ERROR_REACCION_NO_ENCONTRADA = "No se encontro la reacción a eliminar"

muro_bp = Blueprint("muro", __name__, url_prefix="/api/muro")
repositorio = MongoPublicacionRepository()


def obtener_usuario_por_alias(alias: str):
    """
    Extrae la lógica de búsqueda de usuario por alias.
    
    Args:
        alias: Alias del usuario a buscar
        
    Returns:
        UserDocument o None si no se encuentra
    """
    return UserDocument.objects(alias=alias).first()


def validar_contenido(contenido: str) -> tuple:
    """
    Valida que el contenido no esté vacío.
    
    Args:
        contenido: Contenido a validar
        
    Returns:
        Tuple (es_valido: bool, mensaje_error: str o None)
    """
    if not contenido:
        return False, ERROR_CONTENIDO_VACIO
    return True, None


def crear_respuesta_publicacion(publicacion, reacciones):
    """
    Crea el diccionario de respuesta para una publicación.
    
    Args:
        publicacion: Objeto de publicación
        reacciones: Diccionario de reacciones
        
    Returns:
        Diccionario con los datos de la publicación
    """
    return {
        "id": publicacion.id,
        "contenido": publicacion.contenido,
        "fecha_creacion": publicacion.fecha_creacion.isoformat(),
        "reacciones": reacciones,
        "anonimo": publicacion.anonimo
    }


@muro_bp.route("/", methods=["POST"])
@jwt_required()
def crear_publicacion():
    data = request.get_json()
    contenido = data.get("contenido", "").strip()
    anonimo = data.get("anonimo", False)

    # Validar contenido
    es_valido, mensaje_error = validar_contenido(contenido)
    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    # Obtener usuario
    user_id = get_jwt_identity()
    autor = obtener_usuario_por_alias(user_id)
    if not autor:
        return jsonify({"error": ERROR_USUARIO_NO_ENCONTRADO}), 404

    # Crear publicación
    use_case = CrearPublicacionUseCase(MongoPublicacionRepository())
    nueva_publicacion = use_case.execute(contenido, autor, anonimo)

    # Obtener reacciones
    reacciones_repo = MongoReaccionRepository()
    reacciones = reacciones_repo.contar_por_tipo(nueva_publicacion.id)

    return jsonify(crear_respuesta_publicacion(nueva_publicacion, reacciones)), 201


@muro_bp.route("/", methods=["GET"])
def obtener_publicaciones():
    use_case = ObtenerPublicacionesUseCase(MongoPublicacionRepository())
    publicaciones = use_case.execute()

    reacciones_repo = MongoReaccionRepository()
    publicaciones_json = []

    for publicacion in publicaciones:
        reacciones = reacciones_repo.contar_por_tipo(publicacion.id)
        publicaciones_json.append({
            "id": publicacion.id,
            "contenido": publicacion.contenido,
            "fecha_creacion": publicacion.fecha_creacion.isoformat(),
            "fecha_actualizacion": publicacion.fecha_actualizacion.isoformat(),
            "reacciones": reacciones,
            "usuario": publicacion.usuario,
            "anonimo": publicacion.anonimo
        })

    return jsonify(publicaciones_json), 200


@muro_bp.route("/<publicacion_id>", methods=["PATCH"])
@jwt_required()
def editar_publicacion(publicacion_id):
    data = request.get_json()
    nuevo_contenido = data.get("contenido", "").strip()

    # Validar contenido
    es_valido, mensaje_error = validar_contenido(nuevo_contenido)
    if not es_valido:
        return jsonify({"error": mensaje_error}), 400

    # Editar publicación
    autor_alias = get_jwt_identity()
    use_case = EditarPublicacionUseCase(MongoPublicacionRepository())
    resultado = use_case.execute(publicacion_id, nuevo_contenido, autor_alias)

    if not resultado:
        return jsonify({"error": ERROR_SIN_PERMISOS_EDITAR}), 403

    return jsonify({"mensaje": "Publicación editada correctamente"}), 200


@muro_bp.route("/<publicacion_id>", methods=["DELETE"])
@jwt_required()
def eliminar_publicacion(publicacion_id):
    autor_alias = get_jwt_identity()
    use_case = EliminarPublicacionUseCase(MongoPublicacionRepository())
    resultado = use_case.execute(publicacion_id, autor_alias)

    if resultado:
        return jsonify({"mensaje": "Publicación eliminada correctamente"}), 200
    else:
        return jsonify({"error": ERROR_SIN_PERMISOS_ELIMINAR}), 403


@muro_bp.route("/<publicacion_id>/reaccionar", methods=["POST"])
@jwt_required()
def reaccionar_publicacion(publicacion_id):
    data = request.get_json()
    tipo = data.get("reaccion", "").strip()

    # Obtener usuario
    usuario_alias = get_jwt_identity()
    usuario = obtener_usuario_por_alias(usuario_alias)
    if not usuario:
        return jsonify({"error": ERROR_USUARIO_NO_ENCONTRADO}), 404

    # Registrar reacción
    use_case = ReaccionarPublicacionUseCase(MongoReaccionRepository())
    resultado = use_case.execute(usuario.id, publicacion_id, tipo)

    if not resultado:
        return jsonify({"error": ERROR_YA_REACCIONADO}), 403

    return jsonify({"mensaje": f"Reacción '{tipo}' registrada"}), 200


@muro_bp.route("/<publicacion_id>/reaccionar", methods=["DELETE"])
@jwt_required()
def eliminar_reaccion(publicacion_id):
    data = request.get_json()
    tipo = data.get("reaccion", "").strip()

    # Obtener usuario
    usuario_alias = get_jwt_identity()
    usuario = obtener_usuario_por_alias(usuario_alias)
    if not usuario:
        return jsonify({"error": ERROR_USUARIO_NO_ENCONTRADO}), 404

    # Eliminar reacción
    use_case = EliminarReaccionUseCase(MongoReaccionRepository())
    resultado = use_case.execute(usuario.id, publicacion_id, tipo)

    if not resultado:
        return jsonify({"error": ERROR_REACCION_NO_ENCONTRADA}), 404

    return jsonify({"mensaje": f"Reacción '{tipo}' eliminada"}), 200