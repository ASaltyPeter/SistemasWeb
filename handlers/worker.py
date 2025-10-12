import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
firehose = boto3.client('firehose')
sns = boto3.client('sns')

NOME_TABELA = os.environ.get('ORDER_TABLE')
NOME_FIREHOSE = os.environ.get('FIREHOSE_STREAM')
ARN_TOPICO = os.environ.get('NOTIFY_TOPIC')

def lambda_handler(event, context):
    """Worker Lambda acionado pelo SQS. Processa registros da fila."""
    logger.info('Evento SQS recebido: %s', json.dumps(event))
    tabela = dynamodb.Table(NOME_TABELA)
    
    for registro in event.get('Records', []):
        try:
            corpo = json.loads(registro.get('body') or "{}")
            pedido_id = corpo.get('id')

            # Marca como processado no DynamoDB
            tabela.update_item(
                Key={'id': pedido_id},
                UpdateExpression='SET processado = :p',
                ExpressionAttributeValues={':p': True}
            )
            
            # Envia para o Firehose para análise (opcional)
            if NOME_FIREHOSE:
                dados_para_firehose = json.dumps(corpo) + "\n"
                firehose.put_record(
                    DeliveryStreamName=NOME_FIREHOSE, 
                    Record={'Data': dados_para_firehose.encode('utf-8')}
                )

            # Notifica via SNS (opcional)
            if ARN_TOPICO:
                sns.publish(TopicArn=ARN_TOPICO, Message=f"Pedido {pedido_id} foi processado.")

            logger.info('Pedido %s processado com sucesso.', pedido_id)
            
        except Exception as e:
            logger.exception('Falha ao processar o registro: %s', e)
            # Deixa o Lambda/SQS lidar com a nova tentativa e a DLQ (Dead-Letter Queue)
            raise

    return {'status': 'ok'}
