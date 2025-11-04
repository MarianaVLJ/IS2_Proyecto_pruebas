from mongoengine import connect
from app.config.settings import settings


def init_db():
    if not settings.MONGO_URI:
        raise ValueError("MONGO_URI no esta definido en el archivo .env")
    connect(host=settings.MONGO_URI)
