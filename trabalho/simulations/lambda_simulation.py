from sqs_simulation import receber_mensagens

def lambda_handler(event=None, context=None):
    mensagens = receber_mensagens()
    for msg in mensagens:
        print(f"Lambda processou: {msg}")
    return {"statusCode": 200, "body": "Mensagens processadas"}

if __name__ == "__main__":
    lambda_handler()
