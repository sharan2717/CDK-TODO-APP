
import boto3
import os
import json
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb_client = boto3.client("dynamodb")

def main(event,context):
  try :
     table = os.environ.get("TABLE_NAME")
     logger.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
     if event["body"] :
        task = json.loads(event["body"])
        dynamodb_client.put_item(
            TableName=table,
            Item={
                "id": {"S": str(uuid.uuid4())},
                "task": {"S": task["task"]},
                "completed": {"BOOL": False},
            },
        )
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "task inserted successfully"}),
        }
     else:
        logger.info("## Received request without a payload")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "no payload found"}),
        }
  except Exception as e:
        logger.error(f"## Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"Error": str(e)}),
        }   