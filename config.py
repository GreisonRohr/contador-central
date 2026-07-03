import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Ajuste necessário para o Render
        database_url = database_url.replace("postgres://", "postgresql://", 1)

        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            BASE_DIR,
            "database",
            "contador.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "contador-central-2026"
    )