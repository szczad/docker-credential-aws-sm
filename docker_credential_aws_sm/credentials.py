#!/usr/bin/env python

from __future__ import absolute_import, print_function

import os
import sys
import json
import boto3


class DockerAWSCredentialHelper(object):

    def __init__(self, secret_name, secret_key_arn=None, stdin=sys.stdin, stdout=sys.stdout):
        self.__input = stdin
        self.__output = stdout
        self.__secret_name = secret_name
        self.__key_arn = secret_key_arn

        self.__client = boto3.session.Session().client('secretsmanager')

    def list(self):
        data = dict([(url, credentials['username']) for url, credentials in self.__get_secrets().items()])
        self.__write(json.dumps(data))

    def get(self):
        url = self.__read()
        if not url:
            raise ValueError('Invalid credentials provided')

        secret = self.__get_secrets()
        if url not in secret:
            return

        response = {
            'ServerURL': url,
            'Username': secret[url]['username'],
            'Secret': secret[url]['password']
        }
        self.__write(json.dumps(response))

    def store(self):
        create_secret = False
        try:
            _in = json.loads(self.__read())
        except TypeError:
            _in = {}

        try:
            data = self.__get_secrets()
        except Exception as e:
            create_secret = True
            data = {}

        data[_in['ServerURL']] = {
            'username': _in['Username'],
            'password': _in['Secret']
        }
        self.__set_secrets(data, create_secret)

    def erase(self):
        url = self.__read()
        data = self.__get_secrets()
        if url in data:
            del data[url]
            self.__set_secrets(data)

    def __read(self):
        with self.__input as i:
            return "".join(map(str.strip, i.readlines()))

    def __write(self, data):
        with self.__output as o:
            o.writelines(data)

    def __get_secrets(self):
        content = self.__client.get_secret_value(SecretId=self.__secret_name)
        if not content or content['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise ValueError('Invalid response from the server: {}'.format(content['ResponseMetadata']['HTTPStatusCode']))

        return json.loads(content['SecretString'])

    def __set_secrets(self, values, create_secret=False):
        content = json.dumps(values)
        if create_secret:
            kwargs = dict(Name=self.__secret_name, SecretString=content)
            if self.__key_arn:
                kwargs['KmsKeyId'] = self.__key_arn
            self.__client.create_secret(**kwargs)
        else:
            self.__client.put_secret_value(SecretId=self.__secret_name, SecretString=content)


def main():
    """
        ENV variables:
         - DOCKER_SECRETSMANAGER_NAME - variable containing secret name with path for this cluster
         - DOCKER_SECRETSMANAGER_KEY_ARN - ARN of the KMS KEY used to encrypt the secret
        Additional variables for BOTO3 must be set alongside for the tool to work (AWS_PROFILE, AWS_SECRET_KEY_ID, etc.)
    """

    if len(sys.argv) != 2:
        raise ValueError('Invalid number of arguments')

    operation = sys.argv[1]
    if operation.lower() not in ('store', 'get', 'erase', 'list'):
        raise ValueError('Invalid operation provided: {}'.format(operation))

    name = os.environ.get('DOCKER_SECRETSMANAGER_NAME', None)
    if not name:
        raise EnvironmentError('DOCKER_SECRETSMANAGER_NAME not set or invalid')

    key = os.environ.get('DOCKER_SECRETSMANAGER_KEY_ARN', None)
    cred = DockerAWSCredentialHelper(name, key)
    getattr(cred, operation)()


if __name__ == '__main__':
    main()
