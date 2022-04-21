from aws_cdk import (
    # Duration,
    Stack,
    Tags,
    aws_ec2 as ec2, aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns
    # aws_sqs as sqs,
)
from constructs import Construct

class KafkaEcsDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        vpc = ec2.Vpc(self, "Kafka-ECS-Demo", max_azs=2)     # default is all AZs in region

        cluster = ecs.Cluster(self, "KafKa-ECS", vpc=vpc)

        ecs_patterns.ApplicationLoadBalancedFargateService(self, "KafkaFargate",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=6,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(
                    directory='.', 
                    exclude=['cdk.out'])),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True)  # Default is False

        
        Tags.of(self).add('Application', 'kafka-ecs-test')
        Tags.of(self).add('Environment', 'dev') 
        Tags.of(self).add('Name', 'ecs') 
        Tags.of(self).add('Team', 'CloudOps')     
    

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "KafkaEcsDemoQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
