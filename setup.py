#!/usr/bin/env python2

from __future__ import absolute_import

from setuptools import setup, find_packages


setup(
    name=u'docker-credential-aws-sm',
    version=u'0.1',

    description=u'Allows storing Docker registry credentials using AWS SecretsManager',
    long_description=open('README.rst').read(),

    author=u'Grzegorz Szczudlik',
    license=u'MIT',
    url=u'https://github.com/szczad/docker-credential-aws-sm',

    keywords=['docker', 'credentials', 'aws', 'secretsmanager'],

    packages=find_packages(),
    install_requires=[
        'boto3'
    ],
    entry_points={
        'console_scripts': [
            'docker-credential-aws-sm = docker_credential_aws_sm.credentials:main'
        ]
    },
)
