from typing import Any, Dict

from app.config import settings
from services import dynamodb_service as db


def _ok(body: Any, status: int = 200) -> Dict[str, Any]:
    return {"statusCode": status, "body": body}


def get_catalog(event, context):
    items = db.scan_table(settings.dynamodb_catalog_table)
    return _ok({"items": items})


def get_catalog_item(event, context):
    item_id = event.get("pathParameters", {}).get("id")
    if not item_id:
        return _ok({"message": "id is required"}, 400)
    item = db.get_item(settings.dynamodb_catalog_table, {"id": item_id})
    if not item:
        return _ok({"message": "not found"}, 404)
    return _ok(item)




