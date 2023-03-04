import uuid
from typing import List, Optional, Dict

from aws_cdk import (
    aws_codebuild as codebuild,
    aws_iam as iam,
    aws_codepipeline_actions as codepipeline_actions
)


def create_project_from_commands(construct, id_, commands: List[str], role_managed_policy_names: List[str] = None,
                                 role_inline_policies: List[iam.Policy] = None,
                                 role_policy_statements: List[iam.PolicyStatement] = None, **kwargs):
    role_managed_policy_names = role_managed_policy_names or []
    role_inline_policies = role_inline_policies or []
    role_policy_statements = role_policy_statements or []
    project = codebuild.PipelineProject(
        construct, id_,
        environment=codebuild.BuildEnvironment(
            build_image=codebuild.LinuxBuildImage.STANDARD_6_0
        ),
        build_spec=codebuild.BuildSpec.from_object({
            "version": "0.2",
            "phases": {
                "build": {
                    "commands": commands
                }
            }
        }),
        **kwargs
    )

    for policy in role_managed_policy_names:
        project.role.add_managed_policy(iam.ManagedPolicy.from_managed_policy_name(policy))

    for policy in role_inline_policies:
        project.role.attach_inline_policy(policy)

    for statement in role_policy_statements:
        project.add_to_role_policy(statement)

    return project


class ShellAction(codepipeline_actions.CodeBuildAction):
    def __init__(self, construct, commands, id_: Optional[str] = None, project_name: Optional[str] = None,
                 role_managed_policy_names: List[str] = None,
                 role_inline_policies: List[iam.Policy] = None,
                 role_policy_statements: List[iam.PolicyStatement] = None, codebuild_kwargs: Optional[Dict] = None,
                 *args, **kwargs):
        id_ = id_ or f"ShellAction{uuid.uuid4()}"
        project_name = project_name or f"shell-action-{uuid.uuid4()}"
        project = create_project_from_commands(
            construct, id_, commands, role_managed_policy_names,
            role_inline_policies, role_policy_statements, project_name=project_name, **codebuild_kwargs
        )
        super().__init__(
            project=project,
            *args,
            **kwargs,
        )
