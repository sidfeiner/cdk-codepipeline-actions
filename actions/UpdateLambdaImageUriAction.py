from typing import Optional
from aws_cdk import (
    aws_iam as iam,
    aws_codebuild as codebuild
)
from constructs import Construct

from actions.ShellAction import ShellAction


class UpdateLambdaImageUriAction(ShellAction):
    def __init__(self, construct: Construct, id_, *, lambda_name: str, image_uri: str,
                 codebuild_project_name: Optional[str], **kwargs):
        account_id = construct.account
        region = construct.region
        policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["lambda:UpdateFunctionCode"],
            resources=[f"arn:aws:lambda:{region}:{account_id}:function:{lambda_name}"]
        )
        super().__init__(
            construct, id_=id_,
            commands=[
                f'aws lambda update-function-code --function-name ${{LAMBDA_FUNC_NAME}} --image-uri "{image_uri}"'
            ],
            role_policy_statements=[policy_statement],
            project_name=codebuild_project_name,
            codebuild_kwargs={'environment_variables': {
                'LAMBDA_FUNC_NAME': codebuild.BuildEnvironmentVariable(value=lambda_name)
            }},
            **kwargs
        )
