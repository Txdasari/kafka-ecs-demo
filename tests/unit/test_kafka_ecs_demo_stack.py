import aws_cdk as core
import aws_cdk.assertions as assertions

from kafka_ecs_demo.kafka_ecs_demo_stack import KafkaEcsDemoStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kafka_ecs_demo/kafka_ecs_demo_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KafkaEcsDemoStack(app, "kafka-ecs-demo")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
