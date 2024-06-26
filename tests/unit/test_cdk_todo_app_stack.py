import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_todo_app.cdk_todo_app_stack import CdkTodoAppStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_todo_app/cdk_todo_app_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkTodoAppStack(app, "cdk-todo-app")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
