import os
import boto3
import uuid
from moto import mock_aws

from lambdas.lambda_recommendations import get_recommendations


@mock_aws
def test_get_recommendations():
    # Configurar variáveis de ambiente para usar o mock
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["LOCALSTACK_URL"] = "http://moto.mock"
    os.environ["DYNAMODB_ENDPOINT"] = "http://moto.mock"
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    table = ddb.create_table(
        TableName="catalog",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    table.wait_until_exists()

    for i in range(3):
        table.put_item(Item={"id": str(uuid.uuid4()), "title": f"T{i}", "genre": "G"})

    res = get_recommendations({"pathParameters": {"userId": "u1"}}, {})
    assert res["statusCode"] == 200
    assert len(res["body"]["recommendations"]) == 3




