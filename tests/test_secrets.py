import unittest
import os
import shutil
import inspect
from unittest.mock import patch, MagicMock
from datacoco_secretsmanager.secrets import SecretsManager

class TestSecretManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sm = SecretsManager()
        cls.settings = {
            'aws_access_key_id': 'aws_key',
            'aws_secret_access_key':'aws_secret',
            'aws_session_token': 'aws_arn_role'
        }

    @patch('datacoco_secretsmanager.secrets.SecretsManager.assume_role')
    def test_assume_role(self, mock_assume_role):
        mock_assume_role.return_value = self.settings

        sm = SecretsManager(
            aws_access_key_id='aws_key',
            aws_secret_access_key='aws_secret',
            aws_role_arn='aws_arn:test:iam::xxxxxx:role/test',
        )
        self.assertEqual(sm.assume_role(), self.settings)

    @patch('datacoco_secretsmanager.secrets.SecretsManager.assume_role')
    @patch('datacoco_secretsmanager.secrets.SecretsManager.get_secret')
    def test_get_config(self, mock_get_secret, mock_assume_role):

        secrets = {
            'config1': 'data/shared/qa/config1',
            'config2': 'data/shared/test/config2'
        }

        config1_secret = {
            'db_name': 'xxxx',
            'user': 'xxxx',
            'host': 'xxx.com',
            'port': '5439',
            'password': 'xxxx',
            'type': 'postgres'
        }
        config2_secret = {
            'type': 'mssql',
            'server': 'xxxx',
            'db_name': 'config2_db',
            'user': 'xxx',
            'password': 'xxx'
        }

        exepected_result = {
            'config1': {
                'db_name': 'xxxx',
                'user': 'xxxx',
                'host': 'xxx.com',
                'port': '5439',
                'password': 'xxxx',
                'type': 'postgres'
            },
            'config2': {
                'type': 'mssql',
                'server': 'xxxx',
                'db_name': 'config2_db',
                'user': 'xxx',
                'password': 'xxx'
            }
        }

        mock_assume_role.return_value = self.settings
        mock_get_secret.side_effect = [ secrets, config1_secret, config2_secret]
        sm = SecretsManager(
            aws_access_key_id='aws_key',
            aws_secret_access_key='aws_secret',
            aws_role_arn='aws_arn:test:iam::xxxxxx:role/test',
        )
        result = sm.get_config('hamb')
        self.assertDictEqual(result, exepected_result)
