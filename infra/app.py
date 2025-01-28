from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elbv2,
    aws_iam as iam,
)
from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create a VPC with default settings
        vpc = ec2.Vpc(self, "VPC", max_azs=2)

        # Create an ECS cluster within the VPC
        cluster = ecs.Cluster(self, "Youtube Cluster", vpc=vpc)

        # Define the ECS task role with required permissions
        task_role = iam.Role(
            self,
            "EcsTaskExecutionRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AmazonECSTaskExecutionRolePolicy"
                )
            ],
        )

        # Define an ECS Task with Fargate launch type
        task_definition = ecs.FargateTaskDefinition(
            self, "MyTaskDef", memory_limit_mib=512, cpu=256, execution_role=task_role
        )

        # Add container to the task definition
        container = task_definition.add_container(
            "MyContainer",
            image=ecs.ContainerImage.from_registry("nginx:latest"),
            memory_limit_mib=512,
            logging=ecs.LogDrivers.aws_logs(stream_prefix="MyApp"),
        )

        # Expose container port
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        # Create the ECS service with a Network Load Balancer (NLB)
        service = ecs_patterns.NetworkLoadBalancedFargateService(
            self,
            "MyFargateService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,  # Expose externally
        )

        # Adjust the listener to listen on port 80
        listener = service.load_balancer.add_listener("Listener", port=80)

        # Add targets to listener
        listener.add_targets("EcsTarget", port=80, targets=[service.service])

        # Output the load balancer DNS name
        self.output = self.node.try_get_context("output")
        self.output["LoadBalancerDNS"] = service.load_balancer.load_balancer_dns_name
