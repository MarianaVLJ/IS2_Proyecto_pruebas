from flask import Flask
from app.config.database import init_db
from app.interfaces.http.auth_routes import auth_bp

# 1. Inicialización de DB solo para este contexto [cite: 224]
init_db()
app = Flask(__name__)

# 2. Registro de rutas de autenticación (Desacopladas) [cite: 272]
app.register_blueprint(auth_bp, url_prefix='/api/auth')

if __name__ == '__main__':
    # 3. Despliegue independiente en puerto 5001
    print("Microservicio de Usuarios corriendo en puerto 5001...")
    app.run(debug=True, port=5001)