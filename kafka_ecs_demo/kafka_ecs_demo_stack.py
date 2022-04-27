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

        # docker_build_asset_options = DockerImageAsset(
        #     build_args={
        #         "build_args_key": "buildArgs"
        #     },
        #     file="Dockerfile",
        #     #image_path="imagePath",
        #     #output_path="outputPath",
        #     platform="linux/amd64" 
        # )

        # frontend_asset = DockerImageAsset(
        #     self, "frontend", directory="./service", file="Dockerfile"
        # )


        # task_definition = ecs.FargateTaskDefinition( self, "kafka-consumer-test", 
        #         cpu=512, memory_limit_mib=2048)

        # image = ecs.ContainerImage.from_registry("springio/gs-spring-boot-docker")
        # container = task_definition.add_container( "spring-boot-container", image=image)

        # port_mapping = ecs.PortMapping(container_port=8080, host_port=8080)
        # container.add_port_mappings(port_mapping)

        # ecs_patterns.ApplicationLoadBalancedFargateService(self, "some-service",
        #     cluster=cluster,
        #     task_definition=task_definition,
        #     desired_count=2,
        #     cpu=512,
        #     memory_limit_mib=2048,
        #     public_load_balancer=True)


        ecs_patterns.ApplicationLoadBalancedFargateService(self, "KafkaFargate",
            cluster=cluster,            # Required
            cpu=512,                    # Default is 256
            desired_count=1,            # Default is 1
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                #image=ecs.ContainerImage.from_docker_image_asset(frontend_asset),
                #image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")),
                #image=ecs.ContainerImage.from_registry("ecs/amazon-ecs-agent")),
                image=ecs.ContainerImage.from_asset(
                   build_args={
                    "platform": "linux/amd64"
                    },
                    directory='.', 
                    exclude=['cdk.out'])),
            memory_limit_mib=2048,      # Default is 512
            public_load_balancer=True,
            )  # Default is False

        
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
