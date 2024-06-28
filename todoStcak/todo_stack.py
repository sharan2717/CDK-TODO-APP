
from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications,
    Stack,
    aws_dynamodb as _dynamodb,
    aws_apigateway as _apigw

)
from constructs import Construct

class TodoStack(Stack):

     def __init__(self,scope : Construct , id :str)->None :
          
           super().__init__(scope,id)

           dynamodbTable= _dynamodb.TableV2(self,"Table",
                                            partition_key=_dynamodb.Attribute(name="id",type=_dynamodb.AttributeType.STRING),
                                           )
           createTask_lambda = _lambda.Function(self, "createTask_lambda" , 
                                       code= _lambda.Code.from_asset('./lambdas'),
                                       handler="create_task.main",
                                       runtime = _lambda.Runtime.PYTHON_3_9,
                                       environment={
                                           "TABLE_NAME": dynamodbTable.table_name
                                       }
                                       )
           getTasks_lambda = _lambda.Function(self, "getTasks_lambda" , 
                                       code= _lambda.Code.from_asset('./lambdas'),
                                       handler="get_task.main",
                                       runtime = _lambda.Runtime.PYTHON_3_9,
                                       environment={
                                           "TABLE_NAME": dynamodbTable.table_name
                                       }
                                       )
           updateTask_lambda = _lambda.Function(self, "updateTask_lambda" , 
                                       code= _lambda.Code.from_asset('./lambdas'),
                                       handler="update_task.main",
                                       runtime = _lambda.Runtime.PYTHON_3_9,
                                       environment={
                                           "TABLE_NAME": dynamodbTable.table_name
                                       }
                                       )                      

           deleteTask_lambda = _lambda.Function(self, "deleteTask_lambda" , 
                                       code= _lambda.Code.from_asset('./lambdas'),
                                       handler="delete_task.main",
                                       runtime = _lambda.Runtime.PYTHON_3_9,
                                       environment={
                                           "TABLE_NAME": dynamodbTable.table_name
                                       }
                                       )
           dynamodbTable.grant_read_write_data(createTask_lambda)
           dynamodbTable.grant_read_write_data(getTasks_lambda)
           dynamodbTable.grant_read_write_data(updateTask_lambda)
           dynamodbTable.grant_read_write_data(deleteTask_lambda)

           api = _apigw.RestApi(self, "MyApi", rest_api_name="My REST API")
           tasks = api.root.add_resource("tasks")
           tasks.add_method("GET", _apigw.LambdaIntegration(getTasks_lambda))
           tasks.add_method("POST", _apigw.LambdaIntegration(createTask_lambda))
           tasks.add_method("PUT", _apigw.LambdaIntegration(updateTask_lambda))
           tasks.add_method("DELETE", _apigw.LambdaIntegration(deleteTask_lambda))


