
import boto3
import os
import json
import logging
import uuid

dynamodb_client = boto3.client("dynamodb")

def handler(event):
  try :
     table = os.environ.get("TABLE_NAME")
     logging.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
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
        logging.info("## Received request without a payload")
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "no payload found"}),
        }
  except Exception as e:
        logging.error(f"## Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal Server Error"}),
        }   