from sqs_simulation import receber_mensagens

def lambda_handler():
    mensagens = receber_mensagens()
    for msg in mensagens:
        print(f"Lambda processou: {msg}")

if __name__ == "__main__":
    lambda_handler()
