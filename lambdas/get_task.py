import boto3
import os
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

dynamodb_client = boto3.client("dynamodb")

def main(event, context):
    try:
        table = os.environ.get("TABLE_NAME")
        logger.info(f"Loaded table name from environment variable TABLE_NAME: {table}")
        
        response = dynamodb_client.scan(TableName=table)
        tasks = []
        
        for item in response.get('Items', []):
            try:
                task = {
                    "id": item["id"]["S"],
                    "task": item.get("task", {}).get("S", "No task"),
                    "completed": item.get("completed", {}).get("BOOL", False)
                }
                tasks.append(task)
            except KeyError as ke:
                logger.error(f"Missing key: {ke} in item: {item}")
            except Exception as e:
                logger.error(f"Error processing item: {item}, Error: {e}")
        
        logger.info(f"Retrieved tasks: {tasks}")
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(tasks),
        }
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(e)}),
        }

if __name__ == "__main__":
    test_event = {} 
    test_context = {}  
    result = main(test_event, test_context)
    print(result)
