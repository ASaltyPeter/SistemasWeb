import os
import boto3

REGION = os.getenv("AWS_REGION", "us-east-1")
ENDPOINT = os.getenv("DYNAMODB_ENDPOINT", os.getenv("LOCALSTACK_URL", "http://localhost:4566"))

# Configurar credenciais padrão para LocalStack
os.environ.setdefault("AWS_ACCESS_KEY_ID", "test")
os.environ.setdefault("AWS_SECRET_ACCESS_KEY", "test")


def ensure_table(dynamodb, name, key_name):
    existing = [t for t in dynamodb.meta.client.list_tables()["TableNames"]]
    if name in existing:
        return
    dynamodb.create_table(
        TableName=name,
        KeySchema=[{"AttributeName": key_name, "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": key_name, "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    ).wait_until_exists()


def main():
    dynamodb = boto3.resource("dynamodb", region_name=REGION, endpoint_url=ENDPOINT)
    ensure_table(dynamodb, os.getenv("DYNAMODB_CATALOG_TABLE", "catalog"), "id")
    ensure_table(dynamodb, os.getenv("DYNAMODB_USER_VIEWS_TABLE", "user_views"), "userId")
    ensure_table(dynamodb, os.getenv("DYNAMODB_RECO_TABLE", "recommendations"), "userId")


if __name__ == "__main__":
    main()




