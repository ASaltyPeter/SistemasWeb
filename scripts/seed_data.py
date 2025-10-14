import os
import uuid
import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", os.getenv("LOCALSTACK_URL", "http://localhost:4566"))
TABLE = os.getenv("DYNAMODB_CATALOG_TABLE", "catalog")

# Configurar credenciais padrão para LocalStack
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test")

SAMPLES = [
    {"title": "Stranger Things", "genre": "Sci-Fi"},
    {"title": "The Witcher", "genre": "Fantasy"},
    {"title": "Breaking Bad", "genre": "Drama"},
    {"title": "Black Mirror", "genre": "Sci-Fi"},
    {"title": "Money Heist", "genre": "Crime"},
]


def main():
    dynamodb = boto3.resource("dynamodb", region_name=REGION, endpoint_url=ENDPOINT)
    table = dynamodb.Table(TABLE)
    for s in SAMPLES:
        table.put_item(Item={"id": str(uuid.uuid4()), **s})


if __name__ == "__main__":
    main()




