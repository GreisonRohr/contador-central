from flask import Blueprint, jsonify, request
from datetime import datetime

from models import db, Unidade, Impressora, Historico

api = Blueprint("api", __name__)


@api.route("/api/upload", methods=["POST"])
def upload():

    dados = request.get_json()

    # Procura ou cria a unidade
    unidade = Unidade.query.filter_by(
        nome=dados["unidade"]
    ).first()

    if unidade is None:
        unidade = Unidade(
            nome=dados["unidade"],
            ultima_comunicacao=datetime.utcnow()
        )
        db.session.add(unidade)
        db.session.commit()
    else:
        unidade.ultima_comunicacao = datetime.utcnow()

    # Percorre todas as impressoras enviadas
    for item in dados["impressoras"]:

        impressora = Impressora.query.filter_by(
            serial=item["serial"]
        ).first()

        if impressora is None:

            impressora = Impressora(
                unidade_id=unidade.id,
                nome=item["nome"],
                modelo=item["modelo"],
                serial=item["serial"],
                ip=item["ip"],
                contador_atual=item["contador"],
                ultima_leitura=datetime.fromisoformat(item["data"])
            )

            db.session.add(impressora)
            db.session.flush()

        else:

            impressora.nome = item["nome"]
            impressora.modelo = item["modelo"]
            impressora.ip = item["ip"]
            impressora.contador_atual = item["contador"]
            impressora.ultima_leitura = datetime.fromisoformat(item["data"])

        historico = Historico(
            impressora_id=impressora.id,
            contador=item["contador"],
            data_leitura=datetime.fromisoformat(item["data"])
        )

        db.session.add(historico)

    db.session.commit()

    return jsonify({
        "status": "ok"
    })


@api.route("/api/printers", methods=["GET"])
def printers():

    lista = []

    impressoras = Impressora.query.all()

    for p in impressoras:

        lista.append({
            "unidade": p.unidade.nome,
            "nome": p.nome,
            "modelo": p.modelo,
            "serial": p.serial,
            "ip": p.ip,
            "contador": p.contador_atual,
            "ultima_leitura": p.ultima_leitura.isoformat() if p.ultima_leitura else None
        })

    return jsonify(lista)