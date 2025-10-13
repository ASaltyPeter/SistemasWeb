import os
from dataclasses import dataclass


@dataclass
class Settings:
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    localstack_url: str = os.getenv("LOCALSTACK_URL", "http://localhost:4566")

    dynamodb_catalog_table: str = os.getenv("DYNAMODB_CATALOG_TABLE", "catalog")
    dynamodb_user_views_table: str = os.getenv("DYNAMODB_USER_VIEWS_TABLE", "user_views")
    dynamodb_reco_table: str = os.getenv("DYNAMODB_RECO_TABLE", "recommendations")

    sqs_watch_queue_url: str = os.getenv("SQS_WATCH_QUEUE_URL", "http://localhost:4566/000000000000/watch-events-queue")
    sqs_reco_queue_url: str = os.getenv("SQS_RECO_QUEUE_URL", "http://localhost:4566/000000000000/recommendations-queue")


settings = Settings()
