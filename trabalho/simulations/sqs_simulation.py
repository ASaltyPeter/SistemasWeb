# Simulação de Fila SQS (lista Python)
sqs_fila = []

def enviar_mensagem(mensagem):
    sqs_fila.append(mensagem)
    return f"Mensagem enviada para a fila: {mensagem}"

def receber_mensagens():
    return sqs_fila
