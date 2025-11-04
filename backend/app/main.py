from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.interfaces.http.auth_routes import auth_bp
from app.interfaces.http.muro_routes import muro_bp
from app.interfaces.http.denuncia_routes import denuncia_bp
from app.config.settings import settings

jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configuracion de JWT desde settings
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.JWT_ACCESS_TOKEN_EXPIRES
    app.config["SECRET_KEY"] = settings.SECRET_KEY

    # Extensiones
    CORS(app, supports_credentials=True, origins=["http://localhost:5173"])
    jwt.init_app(app)

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(muro_bp)
    app.register_blueprint(denuncia_bp)

    return app
