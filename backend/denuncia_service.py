from flask import Flask
from app.config.database import init_db
from app.interfaces.http.denuncia_routes import denuncia_bp

init_db()
app = Flask(__name__)
# Registramos solo el contexto de denuncias para este servicio
app.register_blueprint(denuncia_bp, url_prefix="/api/denuncias")

if __name__ == "__main__":
    print("Microservicio de Denuncias corriendo en el puerto 5002...")
    app.run(debug=True, port=5002)
