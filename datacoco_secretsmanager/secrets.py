#!/usr/bin/env python
"""
Module provides basic interaction with AWS Secrets Manager service
"""
import ast
import base64
import os
import warnings

import boto3
from boto3.session import Session
from botocore.exceptions import ClientError


class SecretsManager:
    """
    Wrapper on Amazon Web Services' boto3 Secrets Manager
    """

    # pylint: disable=C0330
    def __init__(
        self,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        aws_role_arn=None,
        region_name="us-east-1",
    ):
        """
        :param aws_access_key_id: use to override default credentials or
            assumed role access
        :param aws_secret_access_key: use to override default credentials or
            asuumed role access
        :param aws_role_arn: for assuming role with secrets must be used if
            passing in access keys
        :param region_name: use to override default 'us-east-1' region
        """
        session_kwargs = {"region_name": region_name}

        if aws_access_key_id and aws_secret_access_key:
            if aws_role_arn:
                session_kwargs = self.assume_role(
                    aws_access_key_id,
                    aws_secret_access_key,
                    aws_role_arn,
                    session_kwargs,
                )
            else:
                role_based_warning = (
                    "If role based permissions used in AWS, aws_role_arn "
                    "arg must be provided for access to secrets' resource(s)."
                )
                warnings.warn(role_based_warning)
                session_kwargs["aws_access_key_id"] = aws_access_key_id
                session_kwargs["aws_secret_access_key"] = aws_secret_access_key

        self.session = Session(**session_kwargs)

        # Create a Secrets Manager client
        self.client = self.session.client(service_name="secretsmanager")
        print("Connected to Secrets Manager client")

    def assume_role(self, access_key_id, secret_access_key, arn, kwargs):
        """Assume role via boto3 for access to resources.

        To be used for directly passing in access keys.

        :param aws_access_key_id: use to override default credentials or
            assumed role access
        :param aws_secret_access_key: use to override default credentials or
            assumed role access
        :param aws_role_arn: for assuming role with secrets must be used if
            passing in access keys
        """
        arn_id = arn.split(":")[4]
        session_name = "sm_assumed_role_session_{}".format(arn_id)
        sts_client = boto3.client(
            service_name="sts",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
        )
        assumed_role_object = sts_client.assume_role(
            RoleArn=arn, RoleSessionName=session_name
        )
        credentials = assumed_role_object["Credentials"]
        kwargs["aws_access_key_id"] = credentials["AccessKeyId"]
        kwargs["aws_secret_access_key"] = credentials["SecretAccessKey"]
        kwargs["aws_session_token"] = credentials["SessionToken"]

        return kwargs

    def get_secret(self, secret_name):
        """AWS' handler for fetch of secret.

        Additionally parses AWS secret value response into dict.

        :param secret_name: resource name entered in AWS, with credentials
            stored as key(s)/value(s)
        """
        # In this sample we only handle the specific exceptions for the
        # 'GetSecretValue' API.
        # pylint: disable=C0301
        # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html # noqa
        # We rethrow the exception by default.
        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
            secret = ast.literal_eval(
                get_secret_value_response["SecretString"]
            )
            return secret
        except ClientError as e:
            if e.response["Error"]["Code"] == "DecryptionFailureException":
                # Secrets Manager can't decrypt the protected secret text using
                # the provided KMS key.
                # Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
            elif (
                e.response["Error"]["Code"] == "InternalServiceErrorException"
            ):
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidParameterException":
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
            elif e.response["Error"]["Code"] == "InvalidRequestException":
                # You provided a parameter value that is not valid for the
                # current
                # state of the resource.
                # Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
            elif e.response["Error"]["Code"] == "ResourceNotFoundException":
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your
                # discretion.
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary,
            # one of these fields will be populated.
            if "SecretString" in get_secret_value_response:
                secret = get_secret_value_response["SecretString"]
                return secret
            else:
                decoded_binary_secret = base64.b64decode(
                    get_secret_value_response["SecretBinary"]
                )
                return decoded_binary_secret

    def get_config(self, project_name, team_name=None):
        """Fetch full config and credentials for all systems/connections at
        repo/project level.

        Based on whether a team_name and/or environent variable is assigned,
        the following naming is used to find an AWS Secrets resource name:
        {team_name}/{project_name}/{environment}

        :param project_name: repo/project name for config-store resource name
        :param team_name: if team assigned, prefixed to project_name:
            {team_name}/{project_name}
        """
        # If environment assigned, post-fixed to project_name arg
        # {project_name}/{environment}
        environment = os.getenv("ENVIRONMENT", None)

        cfg_store = f"{project_name}"

        if team_name:
            cfg_store = f"{team_name}/{cfg_store}"
        if environment:
            cfg_store = f"{cfg_store}/{environment}"

        print(f"Getting full configuration mapping for cfg_store: {cfg_store}")
        config_lookup = self.get_secret(cfg_store)
        config = {}
        if config_lookup:
            for k, v in config_lookup.items():
                section = self.get_secret(v)
                section_config = {
                    config_item[0]: config_item[1]
                    for config_item in section.items()
                }
                config[k] = section_config
        return config
