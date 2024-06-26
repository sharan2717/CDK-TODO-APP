import boto3
import os
import json
import logging

dynamodb_client = boto3.client("dynamodb")

def handler(event):
     try :
       table = os.environ.get("TABLE_NAME")
       logging.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
       response = dynamodb_client.scan(TableName=table)
       tasks=[]
       for item in response.get('Items', []):
          task = {
              "id": item["id"]["S"],
              "task": item["task"]["S"],
              "completed": item["completed"]["BOOL"]
          }
          tasks.append(task)
       return {
          "statusCode": 200,
          "headers": {"Content-Type": "application/json"},
          "body": json.dumps(tasks),
           }
     except Exception as e:
        logging.error(f"## Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal Server Error"}),
        }