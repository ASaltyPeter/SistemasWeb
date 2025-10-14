import os
import json
from typing import Dict, Any

import boto3
from app.config import settings


def _client():
    return boto3.client(
        "sqs",
        region_name=settings.aws_region,
        endpoint_url=os.getenv("SQS_ENDPOINT", settings.localstack_url),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    )


def send_message(queue_url: str, message: Dict[str, Any]) -> None:
    _client().send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))




