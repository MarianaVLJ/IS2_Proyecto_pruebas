from flask import Blueprint, request, jsonify
from app.application.use_cases.register_user import RegisterUserUseCase
from app.application.use_cases.login_user import LoginUserUseCase
from app.infrastructure.database.user_repo_impl import MongoUserRepository
from flask_jwt_extended import create_access_token


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    alias = data.get('username')
    password = data.get('password')

    if not alias or not password:
        return jsonify({'error': 'Alias y contraseña son requeridos'}), 400

    use_case = RegisterUserUseCase(MongoUserRepository())
    success = use_case.execute(alias, password)

    if not success:
        return jsonify({'error': 'El alias ya está en uso'}), 400

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201


@auth_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    alias = data.get('username')
    password = data.get('password')

    if not alias or not password:
        return jsonify({'error': 'Alias y contraseña son requeridos'}), 400

    use_case = LoginUserUseCase(MongoUserRepository())
    result = use_case.execute(alias, password)

    if result == "Usuario no encontrado":
        return jsonify({'error': result}), 401
    elif result == "Contraseña incorrecta":
        return jsonify({'error': result}), 401
    else:
        access_token = create_access_token(identity=alias)
        return jsonify({
            'message': result, 'token': access_token
            }), 200
