import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")

os.makedirs(DATABASE_DIR, exist_ok=True)


class Config:

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        DATABASE_DIR,
        "contador.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "contador-central-2026"
    )