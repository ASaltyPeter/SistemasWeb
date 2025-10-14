import os
import boto3
import uuid
from moto import mock_aws

from lambdas.lambda_catalog import get_catalog, get_catalog_item


@mock_aws
def test_get_catalog_and_item():
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

    item_id = str(uuid.uuid4())
    table.put_item(Item={"id": item_id, "title": "X", "genre": "G"})

    res = get_catalog({}, {})
    assert res["statusCode"] == 200
    assert len(res["body"]["items"]) == 1

    res2 = get_catalog_item({"pathParameters": {"id": item_id}}, {})
    assert res2["statusCode"] == 200
    assert res2["body"]["id"] == item_id




