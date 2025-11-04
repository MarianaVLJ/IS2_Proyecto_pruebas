from app.config.database import init_db
from app.main import create_app

init_db()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
