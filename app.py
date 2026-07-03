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

    hoje = datetime.now()

    inicio_semana = hoje - timedelta(days=7)
    inicio_mes = hoje.replace(day=1)

    impressoras = Impressora.query.order_by(
        Impressora.ultima_leitura.desc()
    ).all()

    total_unidades = Unidade.query.count()
    total_impressoras = Impressora.query.count()

    total_paginas_semana = 0
    total_paginas_mes = 0

    for p in impressoras:

        # Primeiro contador da semana
        primeiro_semana = (
            Historico.query
            .filter(
                Historico.impressora_id == p.id,
                Historico.data_leitura >= inicio_semana
            )
            .order_by(Historico.data_leitura.asc())
            .first()
        )

        if primeiro_semana:
            p.paginas_semana = max(
                p.contador_atual - primeiro_semana.contador,
                0
            )
        else:
            p.paginas_semana = 0

        # Primeiro contador do mês
        primeiro_mes = (
            Historico.query
            .filter(
                Historico.impressora_id == p.id,
                Historico.data_leitura >= inicio_mes
            )
            .order_by(Historico.data_leitura.asc())
            .first()
        )

        if primeiro_mes:
            p.paginas_mes = max(
                p.contador_atual - primeiro_mes.contador,
                0
            )
        else:
            p.paginas_mes = 0

        total_paginas_semana += p.paginas_semana
        total_paginas_mes += p.paginas_mes

    return render_template(
        "dashboard.html",
        impressoras=impressoras,
        total_unidades=total_unidades,
        total_impressoras=total_impressoras,
        paginas_semana=total_paginas_semana,
        paginas_mes=total_paginas_mes
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )