from typing import Any, Dict

from app.config import settings
from services import dynamodb_service as db
from services import sqs_service


def _ok(body: Any, status: int = 200) -> Dict[str, Any]:
    return {"statusCode": status, "body": body}


def post_watch(event, context):
    body = event.get("body", {})
    user_id = body.get("userId")
    item_id = body.get("itemId")
    if not user_id or not item_id:
        return _ok({"message": "userId and itemId are required"}, 400)

    record = {"userId": user_id, "itemId": item_id}
    db.put_item(settings.dynamodb_user_views_table, record)

    sqs_service.send_message(settings.sqs_watch_queue_url, record)
    return _ok({"message": "accepted"}, 202)




