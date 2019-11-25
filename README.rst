datacoco-secretsmanager
=======================

datacoco-secretsmanager provides basic interaction with the Amazon Web
Service (AWS) Secrets Manager service.

Installation
------------

datacoco-secretsmanager requires Python 3.6+

::

    python3 -m venv venv
    source venv/bin/activate
    python -m pip install datacoco_secretsmanager

Quickstart
----------

If you have AWS credentials stored in the default
``~/.aws/credentials``, instantiate a SecretsManager class using:

::

    from datacoco_secretsmanager import SecretsManager

    sm = SecretsManager()

Otherwise, pass in AWS authentication keys:

::

    from datacoco_secretsmanager import SecretsManager

    sm = SecretsManager(

        aws_access_key_id,

        aws_secret_access_key,

        aws_role_arn, # only required if you are using role based access

    )

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

(Note: If using environment, environment variable named ``ENVIRONMENT``
should be stored.)

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

Contributing
~~~~~~~~~~~~

Contributions to datacoco\_secretsmanager are welcome!

Please reference guidelines to help with setting up your development
environment
`here <https://github.com/equinoxfitness/datacoco-secretsmanager/blob/master/CONTRIBUTING.rst>`__.
