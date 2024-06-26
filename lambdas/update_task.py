
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
     item = json.loads(event["body"])
     id = {'student_id': item['id']} 
     if 'task' in item:
        update_task(id, 'task', item['task'])
     if 'completed' in item:
        update_task(id, 'completed', item['completed'])
     return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Task updated successfully"}),
        }
  except Exception as e:
        logging.error(f"## Error: {e}")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Internal Server Error"}),
        }
def update_task(id,field,value,table):
   try: 
    update_expression = f"SET {field} = :val"
    expression_attribute_values = {
        ':val': value
    }
    response = dynamodb_client.update_item(
        TableName=table,
        Key=id,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ReturnValues="UPDATED_NEW"
    )
   except Exception as e:
        logging.error(f"## Error: {e}")
        raise Exception(f"An error occurred: {str(e)}")


   