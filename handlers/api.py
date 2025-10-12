\
    # handlers/api.py
    import json
    import os
    import uuid
    import boto3
    import logging
    from flask import Flask, request, jsonify
    import awsgi

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    app = Flask(__name__)

    dynamodb = boto3.resource('dynamodb')
    sqs = boto3.client('sqs')
    sns = boto3.client('sns')

    TABLE_NAME = os.environ.get('ORDER_TABLE')
    QUEUE_NAME = os.environ.get('QUEUE_NAME')
    TOPIC_ARN = os.environ.get('NOTIFY_TOPIC')

    @app.route('/order', methods=['POST'])
    def create_order():
        try:
            body = request.get_json(force=True) or {}
            name = body.get("client", "guest")
            items = body.get("items", [])
            total = body.get("total", 0.0)
            order_id = str(uuid.uuid4())
            order_item = {
                "id": order_id,
                "client": name,
                "items": items,
                "total": str(total),
                "delivered": False
            }

            # Persist to DynamoDB
            table = dynamodb.Table(TABLE_NAME)
            table.put_item(Item=order_item)

            # Resolve queue URL by name and send message
            queue_url = sqs.get_queue_url(QueueName=QUEUE_NAME)['QueueUrl']
            sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(order_item))

            # Publish to SNS topic (optional)
            if TOPIC_ARN:
                sns.publish(TopicArn=TOPIC_ARN, Message=f"New order {order_id} by {name}")

            return jsonify({"id": order_id, "message": "order created"})

        except Exception as e:
            logger.exception("Error in create_order endpoint")
            return jsonify({"error": str(e)}), 500

    def lambda_handler(event, context):
        \"\"\"AWS Lambda handler that adapts API Gateway event to Flask via awsgi.\"\"\"
        return awsgi.response(app, event, context)
