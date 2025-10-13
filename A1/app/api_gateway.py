from flask import Flask, jsonify, request

from app.config import settings
from lambdas.lambda_catalog import get_catalog, get_catalog_item
from lambdas.lambda_views import post_watch
from lambdas.lambda_recommendations import get_recommendations


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/catalog")
    def catalog_list():
        result = get_catalog({}, {})
        return jsonify(result["body"]), result["statusCode"]

    @app.get("/catalog/<item_id>")
    def catalog_get(item_id: str):
        result = get_catalog_item({"pathParameters": {"id": item_id}}, {})
        return jsonify(result["body"]), result["statusCode"]

    @app.post("/watch")
    def watch_event():
        payload = request.get_json(force=True, silent=True) or {}
        result = post_watch({"body": payload}, {})
        return jsonify(result["body"]), result["statusCode"]

    @app.get("/recommendations/<user_id>")
    def recommendations(user_id: string):  # type: ignore[name-defined]
        result = get_recommendations({"pathParameters": {"userId": user_id}}, {})
        return jsonify(result["body"]), result["statusCode"]

    return app
