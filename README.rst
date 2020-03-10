datacoco-secretsmanager
=======================

.. image:: https://badge.fury.io/py/datacoco-secretsmanager.svg
    :target: https://badge.fury.io/py/datacoco-secretsmanager
    :alt: PyPI Version

.. image:: https://readthedocs.org/projects/datacoco-secretsmanager/badge/?version=latest
    :target: https://datacoco-secretsmanager.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://api.codacy.com/project/badge/Grade/861b44dcbfdb42f4bcdabea51563ba65
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-secretsmanager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-secretsmanager&amp;utm_campaign=Badge_Grade
    :alt: Code Quality Grade

.. image:: https://api.codacy.com/project/badge/Coverage/861b44dcbfdb42f4bcdabea51563ba65
    :target: https://www.codacy.com/gh/equinoxfitness/datacoco-secretsmanager?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=equinoxfitness/datacoco-secretsmanager&amp;utm_campaign=Badge_Coverage
    :alt: Coverage

.. image:: https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg
    :target: https://github.com/equinoxfitness/datacoco-secretsmanager/blob/master/CODE_OF_CONDUCT.rst
    :alt: Code of Conduct

datacoco-secretsmanager provides basic interaction with the Amazon Web
Service (AWS) Secrets Manager service.

Installation
------------

**datacoco-secretsmanager requires Python 3.6+**

::

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install datacoco_secretsmanager

Quickstart
----------

datacoco-secretsmanager utilizes the `boto3 <https://boto3.amazonaws.com/v1/documentation/api/latest/index.html>`_ library to interact with the AWS Secrets Manager service, requiring AWS credentials configuration. Lookup of credentials by boto3 is documented `here <https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html>`_.

**Based on how you store your AWS credentials, you can use datacoco-secretsmanager in the following ways.**

If you have AWS credentials stored in the default
`~/.aws/credentials <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html>`_, instantiate a SecretsManager class using:

::

    from datacoco_secretsmanager import SecretsManager

    sm = SecretsManager()

You can also pass in AWS authentication keys directly:

::

    from datacoco_secretsmanager import SecretsManager

    sm = SecretsManager(

        aws_access_key_id,

        aws_secret_access_key,

        aws_role_arn, # only required if you are using role based access

    )

Otherwise, if you are running on an Amazon EC2 instance, and credentials are not passed in either way above, you can have boto3 load credentials from the instance metadata service.
datacoco-secretsmanager will then assume the same IAM role as you specified when you launched your EC2 instance.

One Secret
~~~~~~~~~~

Store a secret in AWS Secrets manager:

**AWS Secret name**

::

    <AWS-secret-name-for-connection>

::

    | Key        | Value        |
    | ---------- | -------------|
    | <db-name>  | <db-name>    |
    | <user>     | <user-name>  |
    | <host>     | <host>       |
    | <port>     | <port-value> |
    | ...        | ...          |

To fetch a single secret, use:

::

    sm.get_secret(<aws_secret_resource_name>)

Many Secrets
~~~~~~~~~~~~

For a project, you may have more than one secret or credentials for more
than one system.

You can handle by storing key/value mapping for all required credentials
in an AWS secret for the project, then further store credentials in a
separate AWS secret for each credential name indicated in a key's value.

For example, storing a single AWS secret to map or provide lookup to all
required system/db connections is known as the ``cfg_store`` name in our
module:

**AWS Secret name**

::

    <project-name>/<environment>

Note: If using environment, environment variable named ``ENVIRONMENT``
should be stored and assigned with the same environment name indicated in your AWS secret name.

Additionally, if working in organization with multiple teams using AWS
Secrets Manager, you can further denote secrets per team, by using
naming convention:

::

    <team-name>/<project-name>/<environment>.

Store key/values for your ``cfg_store`` with the following:

::

    | Key                   | Value                               |
    | --------------------- | ----------------------------------- |
    | <db-connection1-name> | <AWS-secret-name-for-db-connection1>|
    | <db-connection2-name> | <AWS-secret-name-for-db-connection2>|

For each Secret value in your cfg\_store, store the full credentials in
an additional AWS Secret, ie:

**AWS Secret name**

::

    <AWS-secret-name-for-db-connection1>

::

    | Key        | Value        |
    | ---------- | -------------|
    | <db-name1> | <db-name1>   |
    | <user>     | <user-name>  |
    | <host>     | <host>       |
    | <port>     | <port-value> |
    | ...        | ...          |

**AWS Secret name**

::

    <AWS-secret-name-for-db-connection2>

::

    | Key        | Value        |
    | ---------- | -------------|
    | <db-name2> | <db-name2>   |
    | <user>     | <user-name>  |
    | <host>     | <host>       |
    | <port>     | <port-value> |
    | ...        | ...          |

To fetch secrets for a full project/cfg store, use:

::

    sm.get_config(

        project_name='your-project-name',

        team_name='your-team-name',     # include only if you want to save as part of your cfg_store name

    )

Development
-----------

Getting Started
~~~~~~~~~~~~~~~

It is recommended to use the steps below to set up a virtual environment for development:

::

    python3 -m venv <virtual env name>
    source <virtual env name>/bin/activate
    pip install -r requirements.txt

Testing
~~~~~~~

::

    pip install -r requirements-dev.txt

To run the testing suite, simply run the command: ``tox`` or ``python -m unittest discover tests``

Contributing
~~~~~~~~~~~~

Contributions to datacoco\_secretsmanager are welcome!

Please reference guidelines to help with setting up your development
environment
`here <https://github.com/equinoxfitness/datacoco-secretsmanager/blob/master/CONTRIBUTING.rst>`__.
