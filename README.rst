Docker Credentials helper to AWS SecretsManager
===============================================

About
-----

This `helper`_ is suitable for storing Docker registry credentials for distributed Docker installations across
AWS EC2 clouds. It stores all necessary information in JSON in single secret managed by AWS SecretsManager service.

Requirements
------------

The only required software is `boto3`_

Installation
------------
Install package using ``pip``

.. code-block:: console

    pip install docker-credential-aws-sm

Setup
-----
There are 3 steps required before you can use the helper in the cloud

1. To register `helper`_ for current user edit ``$HOME/.docker.config.json`` and place configuration required configuration:

.. code-block:: json

    {
      "credStore": "aws-sm"
    }

For automatic repository discovery configuration should also contain ``"HttpHeaders"`` key:

.. code-block:: json

    {
      "credStore": "aws-sm",
      "HttpHeaders": {
        "User-Agent": "Docker-Client/18.09.1 (linux)"
      }
    }

2. Export necessary environmental variables. ``DOCKER_SECRETSMANAGER_NAME`` is mandatory, ``AWS_`` variables should be set according to needs:

.. code-block:: console

    # (required) DOCKER_SECRETSMANAGER_NAME points the secret name under which the tool stores credentials
    export DOCKER_SECRETSMANAGER_NAME='my_docker_sercret'
    # (optional)
    export AWS_...

3. Create IAM user or role according to your need.

.. _`helper`: https://github.com/szczad/docker-credential-aws-sm
.. _`boto3`: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html

