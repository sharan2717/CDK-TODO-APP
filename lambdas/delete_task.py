import boto3
import os
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb_client = boto3.client("dynamodb")

def main(event,context):
     try :
       table = os.environ.get("TABLE_NAME")
       logger.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
       if event.get("queryStringParameters") and "id" in event["queryStringParameters"]:
            task_id = event["queryStringParameters"]["id"]
       response = dynamodb_client.delete_item(
            TableName=table,
            Key={
                "id": {"S": task_id} 
            }
        )
       return {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": f"Task with ID '{task_id}' deleted successfully"}),
            }
     except Exception as e:
        logger.error(f"## Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"Error": str(e)}),
        }      