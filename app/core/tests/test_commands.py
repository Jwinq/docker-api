"""
    Test Custom Django Management Commands
 """
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """     Test Commands     """
    def test_wait_for_db_ready(self, patched_check):
        """ Simulate dB ready signal"""
        patched_check.return_value = True

        """ Call Command to Check dB"""
        call_command('wait_for_db')

        """ Get the test results"""
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Simulate dB operational error """
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError]*3 + [True]

        """ Call Command to Check dB """
        call_command('wait_for_db')

        """ Count the number of calls """
        self.assertEqual(patched_check.call_count, 6)

        """ Get The Test Results """
        patched_check.assert_called_with(databases=['default'])
