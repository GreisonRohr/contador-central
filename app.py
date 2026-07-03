import os
from datetime import datetime, timedelta

from flask import Flask, render_template

from config import Config
from models import db, Unidade, Impressora, Historico
from api.routes import api

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(api)

# Cria as tabelas automaticamente caso não existam
with app.app_context():
    db.create_all()


@app.route("/")
def dashboard():

    impressoras = Impressora.query.order_by(
        Impressora.ultima_leitura.desc()
    ).all()

    total_unidades = Unidade.query.count()

    total_impressoras = Impressora.query.count()

    inicio_semana = datetime.now() - timedelta(days=7)

    leituras_semana = Historico.query.filter(
        Historico.data_leitura >= inicio_semana
    ).count()

    return render_template(
        "dashboard.html",
        impressoras=impressoras,
        total_unidades=total_unidades,
        total_impressoras=total_impressoras,
        leituras_semana=leituras_semana,
        paginas_semana=0,
        paginas_mes=0
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )