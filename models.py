from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Unidade(db.Model):
    __tablename__ = "unidades"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), unique=True, nullable=False)

    token = db.Column(db.String(100))

    ultima_comunicacao = db.Column(db.DateTime)

    impressoras = db.relationship(
        "Impressora",
        backref="unidade",
        lazy=True,
        cascade="all, delete"
    )


class Impressora(db.Model):
    __tablename__ = "impressoras"

    id = db.Column(db.Integer, primary_key=True)

    unidade_id = db.Column(
        db.Integer,
        db.ForeignKey("unidades.id"),
        nullable=False
    )

    nome = db.Column(db.String(100))

    modelo = db.Column(db.String(100))

    serial = db.Column(db.String(100), unique=True)

    ip = db.Column(db.String(30))

    contador_atual = db.Column(db.Integer)

    ultima_leitura = db.Column(db.DateTime)

    historico = db.relationship(
        "Historico",
        backref="impressora",
        lazy=True,
        cascade="all, delete"
    )


class Historico(db.Model):
    __tablename__ = "historico"

    id = db.Column(db.Integer, primary_key=True)

    impressora_id = db.Column(
        db.Integer,
        db.ForeignKey("impressoras.id"),
        nullable=False
    )

    contador = db.Column(db.Integer)

    data_leitura = db.Column(db.DateTime)

    recebido_em = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )