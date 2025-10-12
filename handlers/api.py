# handlers/api.py
import json
import os
import uuid
import boto3
import logging
from flask import Flask, request, jsonify
import awsgi

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
sns = boto3.client('sns')

NOME_TABELA = os.environ.get('ORDER_TABLE')
NOME_FILA = os.environ.get('QUEUE_NAME')
ARN_TOPICO = os.environ.get('NOTIFY_TOPIC')

@app.route('/pedido', methods=['POST'])
def criar_pedido():
    try:
        corpo = request.get_json(force=True) or {}
        nome_cliente = corpo.get("cliente", "convidado")
        itens = corpo.get("itens", [])
        total = corpo.get("total", 0.0)
        pedido_id = str(uuid.uuid4())
        
        item_pedido = {
            "id": pedido_id,
            "cliente": nome_cliente,
            "itens": itens,
            "total": str(total),
            "processado": False,
            "entregue": False
        }

        # Persiste no DynamoDB
        tabela = dynamodb.Table(NOME_TABELA)
        tabela.put_item(Item=item_pedido)

        # Resolve a URL da fila pelo nome e envia a mensagem
        url_fila = sqs.get_queue_url(QueueName=NOME_FILA)['QueueUrl']
        sqs.send_message(QueueUrl=url_fila, MessageBody=json.dumps(item_pedido))

        # Publica no tópico SNS (opcional)
        if ARN_TOPICO:
            sns.publish(TopicArn=ARN_TOPICO, Message=f"Novo pedido {pedido_id} criado por {nome_cliente}")

        return jsonify({"id": pedido_id, "mensagem": "pedido criado com sucesso"})

    except Exception as e:
        logger.exception("Erro no endpoint /pedido")
        return jsonify({"erro": str(e)}), 500

def lambda_handler(event, context):
    """Handler do AWS Lambda que adapta o evento do API Gateway para o Flask via awsgi."""
    return awsgi.response(app, event, context)
