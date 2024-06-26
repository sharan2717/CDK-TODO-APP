import boto3
import os
import json
import logging

dynamodb_client = boto3.client("dynamodb")

def handler(event):
     try :
       table = os.environ.get("TABLE_NAME")
       logging.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
       if event.get("queryStringParameters") and "id" in event["queryStringParameters"]:
            task_id = event["queryStringParameters"]["id"]
       response = dynamodb_client.delete_item(
            TableName=table,
            Key={
                "id": {"S": task_id}  # Assuming 'id' is a string type primary key
            }
        )
       return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": f"Task with ID '{task_id}' deleted successfully"}),
            }
     except Exception as e:
        logging.error(f"## Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal Server Error"}),
        }      