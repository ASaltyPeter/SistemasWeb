from typing import Dict, Any


def make_view(user_id: str, item_id: str) -> Dict[str, Any]:
    return {"userId": user_id, "itemId": item_id}
