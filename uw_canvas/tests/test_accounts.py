from unittest import TestCase
from commonconf import settings
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.accounts import Accounts as Canvas
from restclients_core.exceptions import DataFailureException
import mock


@fdao_canvas_override
class CanvasTestAccounts(TestCase):
    def test_account(self):
        canvas = Canvas()

        account = canvas.get_account_by_sis_id('uwcourse:seattle:cse:cse')
        self.assertEquals(account.account_id, 696969)
        self.assertEquals(
            account.name, "Computer Science & Engineering", "Has proper name")
        self.assertEquals(account.sis_account_id, 'uwcourse:seattle:cse:cse')
        self.assertEquals(account.parent_account_id, 987654)

    def test_sub_account(self):
        canvas = Canvas()

        accounts = canvas.get_sub_accounts_by_sis_id('uwcourse:seattle:cse')

        account = accounts[1]

        self.assertEquals(len(accounts), 3, "Too few accounts")
        self.assertEquals(
            account.name, "Comp Sci & Engr Accelerated Masters Prg",
            "Has proper name")
        self.assertEquals(account.sis_account_id, 'uwcourse:seattle:cse:csem')
        self.assertEquals(account.parent_account_id, 54321)

    def test_all_sub_accounts(self):
        canvas = Canvas()

        accounts = canvas.get_all_sub_accounts_by_sis_id(
            'uwcourse:seattle:cse')

        account = accounts[1]

        self.assertEquals(len(accounts), 3, "Too few accounts")
        self.assertEquals(
            account.name, "Comp Sci & Engr Accelerated Masters Prg",
            "Has proper name")
        self.assertEquals(account.sis_account_id, 'uwcourse:seattle:cse:csem')
        self.assertEquals(account.parent_account_id, 54321)

    @mock.patch.object(Canvas, '_account_from_json')
    @mock.patch.object(Canvas, '_put_resource')
    def test_update_sis_id(self, mock_update, mock_from_json):
        canvas = Canvas()

        canvas.update_sis_id(54321, 'NEW_SIS_ID')
        mock_update.assert_called_with(
            '/api/v1/accounts/54321',
            {'account': {'sis_account_id': 'NEW_SIS_ID'}})

        # Cannot update sis id for root account
        self.assertRaises(Exception, canvas.update_sis_id,
                          getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID'),
                          'NEW_SIS_ID')
