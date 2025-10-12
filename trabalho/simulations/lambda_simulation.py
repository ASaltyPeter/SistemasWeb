from sqs.sqs_simulation import receber_mensagens
from database.db import salvar_no_banco

def lambda_handler():
    mensagens = receber_mensagens()
    for msg in mensagens:
        print(f"Lambda processou: {msg}")
        salvar_no_banco(msg)  # salva no banco
