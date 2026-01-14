from app.config.database import init_db
from app.main import create_app

from flask import Flask
from app.interfaces.http.swagger import init_swagger

app = Flask(__name__)
init_swagger(app)


init_db()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
