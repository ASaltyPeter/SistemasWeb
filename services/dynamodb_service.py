import os
from typing import Any, Dict, List, Optional

import boto3
from app.config import settings


def _resource():
    return boto3.resource(
        "dynamodb",
        region_name=settings.aws_region,
        endpoint_url=os.getenv("DYNAMODB_ENDPOINT", settings.localstack_url),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    )


def get_table(table_name: str):
    return _resource().Table(table_name)


def put_item(table_name: str, item: Dict[str, Any]) -> None:
    get_table(table_name).put_item(Item=item)


def get_item(table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    response = get_table(table_name).get_item(Key=key)
    return response.get("Item")


def scan_table(table_name: str) -> List[Dict[str, Any]]:
    table = get_table(table_name)
    items: List[Dict[str, Any]] = []
    response = table.scan()
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"]) 
        items.extend(response.get("Items", []))
    return items
