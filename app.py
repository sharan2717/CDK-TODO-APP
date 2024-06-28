#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_todo_app.cdk_todo_app_stack import CdkTodoAppStack
from todoStcak.todo_stack import TodoStack

app = cdk.App()
TodoStack(app, "TodoStack")


app.synth()
