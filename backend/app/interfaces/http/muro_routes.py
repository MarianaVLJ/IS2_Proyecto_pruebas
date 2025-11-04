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

muro_bp = Blueprint("muro", __name__, url_prefix="/api/muro")
repositorio = MongoPublicacionRepository()


@muro_bp.route("/", methods=["POST"])
@jwt_required()
def crear_publicacion():
    data = request.get_json()
    contenido = data.get("contenido", "").strip()
    anonimo = data.get("anonimo", False)

    if not contenido:
        return jsonify({"error": "El contenido no puede estar vacío"}), 400

    user_id = get_jwt_identity()
    autor = UserDocument.objects(alias=user_id).first()
    if not autor:
        return jsonify({"error": "Usuario no encontrado"}), 404

    use_case = CrearPublicacionUseCase(MongoPublicacionRepository())
    nueva_publicacion = use_case.execute(contenido, autor, anonimo)

    reacciones_repo = MongoReaccionRepository()
    reacciones = reacciones_repo.contar_por_tipo(nueva_publicacion.id)

    return jsonify({
        "id": nueva_publicacion.id,
        "contenido": nueva_publicacion.contenido,
        "fecha_creacion": nueva_publicacion.fecha_creacion.isoformat(),
        "reacciones": reacciones,
        "anonimo": nueva_publicacion.anonimo
    }), 201


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

    if not nuevo_contenido:
        return jsonify({"error": "El contenido no puede estar vacío"}), 400

    autor_alias = get_jwt_identity()
    use_case = EditarPublicacionUseCase(MongoPublicacionRepository())

    resultado = use_case.execute(publicacion_id, nuevo_contenido, autor_alias)

    if not resultado:
        return jsonify({
            "error": "No tienes permisos para editar esta publicación"
        }), 403

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
        return jsonify({
            "error": "No tienes permisos para eliminar esta publicación"
        }), 403


@muro_bp.route("/<publicacion_id>/reaccionar", methods=["POST"])
@jwt_required()
def reaccionar_publicacion(publicacion_id):
    data = request.get_json()
    tipo = data.get("reaccion", "").strip()

    usuario_alias = get_jwt_identity()
    usuario = UserDocument.objects(alias=usuario_alias).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    use_case = ReaccionarPublicacionUseCase(MongoReaccionRepository())
    resultado = use_case.execute(usuario.id, publicacion_id, tipo)

    if not resultado:
        return jsonify({"error": "Ya has reaccionado a esta publicación"}), 403

    return jsonify({"mensaje": f"Reacción '{tipo}' registrada"}), 200


@muro_bp.route("/<publicacion_id>/reaccionar", methods=["DELETE"])
@jwt_required()
def eliminar_reaccion(publicacion_id):
    data = request.get_json()
    tipo = data.get("reaccion", "").strip()

    usuario_alias = get_jwt_identity()
    usuario = UserDocument.objects(alias=usuario_alias).first()

    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404

    use_case = EliminarReaccionUseCase(MongoReaccionRepository())
    resultado = use_case.execute(usuario.id, publicacion_id, tipo)

    if not resultado:
        return jsonify({"error": "No se encontro la reacción a eliminar"}), 404

    return jsonify({"mensaje": f"Reacción '{tipo}' eliminada"}), 200
