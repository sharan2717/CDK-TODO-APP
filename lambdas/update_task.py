
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
     item = json.loads(event["body"])
     id = item['id']
     if 'task' in item:
        update_task(id, 'task', item['task'],table)
     if 'completed' in item:
        update_task(id, 'completed', item['completed'],table)
     return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Task updated successfully"}),
        }
  except Exception as e:
        logger.error(f"## Error: {e}")
        print(e)
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"Error": str(e)}),
        }
def update_task(id,field,value,table):
  try: 
        update_expression = f"SET {field} = :val"
        expression_attribute_values = {
            ':val': {'S': value}
        }
        key=  {'id' :{'S': id} }
        response = dynamodb_client.update_item(
        TableName=table,
        Key =key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
    )
  except Exception as e:
        logger.error(f"## Error: {e}")
        raise Exception(f"An error occurred: {str(e)}")


   