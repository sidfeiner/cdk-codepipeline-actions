from typing import List, Optional
from aws_cdk import (
    aws_iam as iam,
    aws_codebuild as codebuild
)
from constructs import Construct

from actions.ShellAction import ShellAction


class InvalidateCloudfrontCacheAction(ShellAction):
    def __init__(self, construct: Construct, id_, *, distribution_id: str, paths: Optional[List[str]] = None,
                 codebuild_project_name: Optional[str], **kwargs):
        paths = paths or ['/*']
        account_id = construct.account
        policy_statement = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["cloudfront:CreateInvalidation"],
            resources=[f"arn:aws:cloudfront::{account_id}:distribution/{distribution_id}"]
        )
        super().__init__(
            construct, id_=id_,
            commands=[
                f"aws cloudfront create-invalidation --distribution-id {distribution_id} --paths {' '.join(paths)}"
            ],
            role_policy_statements=[policy_statement],
            project_name=codebuild_project_name,
            codebuild_kwargs={'environment_variables': {
                "CLOUDFRONT_ID": codebuild.BuildEnvironmentVariable(value=distribution_id)
            }},
            **kwargs
        )
