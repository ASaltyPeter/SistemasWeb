import os
import boto3
from moto import mock_aws

from lambdas.lambda_views import post_watch


@mock_aws
def test_post_watch_enqueues_and_saves():
    # Configurar variáveis de ambiente para usar o mock
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["LOCALSTACK_URL"] = "http://moto.mock"
    os.environ["DYNAMODB_ENDPOINT"] = "http://moto.mock"
    os.environ["SQS_ENDPOINT"] = "http://moto.mock"
    os.environ["AWS_ACCESS_KEY_ID"] = "test"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    ddb.create_table(
        TableName="user_views",
        KeySchema=[{"AttributeName": "userId", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "userId", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    ).wait_until_exists()

    sqs = boto3.client("sqs", region_name="us-east-1")
    qurl = sqs.create_queue(QueueName="watch-events-queue")["QueueUrl"]
    os.environ["SQS_WATCH_QUEUE_URL"] = qurl

    res = post_watch({"body": {"userId": "u1", "itemId": "i1"}}, {})
    assert res["statusCode"] == 202

    msgs = sqs.receive_message(QueueUrl=qurl).get("Messages", [])
    assert len(msgs) == 1




