from typing import Dict, Any, List


def make_recommendations(user_id: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"userId": user_id, "recommendations": items}




