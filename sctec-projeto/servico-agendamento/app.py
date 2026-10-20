from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging
import json
import requests
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sctec.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

logging.basicConfig(
    filename='app.log', 
    level=logging.INFO, 
    format='%(levelname)s:%(asctime)s:%(message)s'
)
logger = logging.getLogger(__name__)

# URL do Serviço Coordenador
COORDENADOR_URL = "http://localhost:3000"

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telescopio_id = db.Column(db.Integer)
    horario_inicio_utc = db.Column(db.DateTime)
    status = db.Column(db.String(20), default="Confirmado")

with app.app_context():
    db.create_all()

@app.route('/agendamentos', methods=['POST'])
def criar_agendamento():
    dados = request.get_json()
    # Criar chave única do recurso
    recurso = f"telescopio_{dados['telescopio_id']}_{dados['horario_inicio_utc']}"
    
    logger.info(f"Requisição recebida para POST /agendamentos. Recurso: {recurso}")
    
    # 1. PEDE PERMISSÃO AO PORTEIRO (NODE)
    logger.info(f"Tentando adquirir lock para o recurso {recurso}")
    try:
        res_lock = requests.post(f"{COORDENADOR_URL}/lock", json={"resource": recurso}, timeout=5)
    except requests.exceptions.ConnectionError:
        logger.error("Coordenador offline!")
        return jsonify({"error": "Coordenador offline"}), 503

    if res_lock.status_code == 409:
        logger.info(f"Falha ao adquirir lock, recurso ocupado.")
        return jsonify({
            "error": "CONFLITO_AGENDA",
            "message": "O horário já está reservado"
        }), 409
    
    logger.info(f"Lock adquirido com sucesso para {recurso}")

    # 2. AÇÃO CRÍTICA (PROTEGIDA PELO LOCK)
    try:
        logger.info("Iniciando verificação de conflito no BD")
        time.sleep(0.5)
        
        logger.info("Salvando novo agendamento no BD")
        novo = Agendamento(
            telescopio_id=dados['telescopio_id'],
            horario_inicio_utc=datetime.fromisoformat(
                dados['horario_inicio_utc'].replace('Z', '+00:00')
            )
        )
        db.session.add(novo)
        db.session.commit()

        # Log de Auditoria
        audit_log = {
            "timestamp_utc": datetime.utcnow().isoformat() + "Z",
            "level": "AUDIT",
            "event_type": "AGENDAMENTO_CRIADO",
            "service": "servico-agendamento",
            "details": {"agendamento_id": novo.id, "recurso": recurso}
        }
        logger.warning(json.dumps(audit_log))

        resposta = {
            "id": novo.id,
            "status": "Confirmado",
            "_links": {
                "self": {"href": f"/agendamentos/{novo.id}"},
                "cancelar": {"href": f"/agendamentos/{novo.id}", "method": "DELETE"},
                "sincronizar_tempo": {"href": "/time"}
            }
        }
        status_code = 201

    finally:
        # 3. LIBERA O LOCK SEMPRE
        logger.info(f"Liberando lock para o recurso {recurso}")
        requests.post(f"{COORDENADOR_URL}/unlock", json={"resource": recurso})

    return jsonify(resposta), status_code

@app.route('/time', methods=['GET'])
def get_time():
    logger.info("Requisição recebida em GET /time")
    return jsonify({"server_time_utc": datetime.utcnow().isoformat() + "Z"})

if __name__ == '__main__':
    app.run(port=5000, threaded=True)
