from typing import Dict, Any


def make_catalog_item(item_id: str, title: str, genre: str) -> Dict[str, Any]:
    return {"id": item_id, "title": title, "genre": genre}




