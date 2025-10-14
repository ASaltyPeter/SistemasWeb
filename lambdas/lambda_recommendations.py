from typing import Any, Dict, List

from app.config import settings
from services import dynamodb_service as db


def _ok(body: Any, status: int = 200) -> Dict[str, Any]:
    return {"statusCode": status, "body": body}


def get_recommendations(event, context):
    user_id = event.get("pathParameters", {}).get("userId")
    if not user_id:
        return _ok({"message": "userId is required"}, 400)

    # naive: recommend first 5 catalog items
    catalog = db.scan_table(settings.dynamodb_catalog_table)
    recs: List[Dict[str, Any]] = catalog[:5]
    return _ok({"userId": user_id, "recommendations": recs})




