import os
import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT = os.getenv("SQS_ENDPOINT", os.getenv("LOCALSTACK_URL", "http://localhost:4566"))

# Configurar credenciais padrão para LocalStack
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test")


def ensure_queue(client, name):
    url = f"{ENDPOINT}/000000000000/{name}"
    try:
        client.get_queue_attributes(QueueUrl=url, AttributeNames=["All"])  # type: ignore[arg-type]
        return url
    except Exception:
        pass
    return client.create_queue(QueueName=name)["QueueUrl"]


def main():
    sqs = boto3.client("sqs", region_name=REGION, endpoint_url=ENDPOINT)
    ensure_queue(sqs, "watch-events-queue")
    ensure_queue(sqs, "recommendations-queue")


if __name__ == "__main__":
    main()




