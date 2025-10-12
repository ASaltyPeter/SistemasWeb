import json
import os
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
firehose = boto3.client('firehose')
sns = boto3.client('sns')

TABLE_NAME = os.environ.get('ORDER_TABLE')
FIREHOSE_NAME = os.environ.get('FIREHOSE_STREAM')
TOPIC_ARN = os.environ.get('NOTIFY_TOPIC')

def lambda_handler(event, context):
    """SQS-triggered Lambda worker. Processes records from the queue.
    Expects event['Records'] with SQS messages.
    """
    logger.info('SQS event received: %s', json.dumps(event))
    table = dynamodb.Table(TABLE_NAME)
    for record in event.get('Records', []):
        try:
            body = json.loads(record.get('body') or "{}")
            order_id = body.get('id')
            # mark as processed in DynamoDB
            table.update_item(
                Key={'id': order_id},
                UpdateExpression='SET processed = :p',
                ExpressionAttributeValues={':p': True}
            )
            # send to Firehose for analytics (optional)
            if FIREHOSE_NAME:
                firehose.put_record(DeliveryStreamName=FIREHOSE_NAME, Record={'Data': json.dumps(body) + "\n"})
            # notify via SNS (optional)
            if TOPIC_ARN:
                sns.publish(TopicArn=TOPIC_ARN, Message=f"Order {order_id} processed")
            logger.info('Processed order %s', order_id)
        except Exception as e:
            logger.exception('Failed to process record: %s', e)
            # Let Lambda/SQS handle retry and DLQ
            raise
    return {'status': 'ok'}
