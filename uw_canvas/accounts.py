# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.models import CanvasAccount, CanvasSSOSettings

ACCOUNTS_API = "/api/v1/accounts/{}"


class Accounts(Canvas):
    def get_account(self, account_id):
        """
        Return account resource for given canvas account id.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show
        """
        url = ACCOUNTS_API.format(account_id)
        return CanvasAccount(data=self._get_resource(url))

    def get_account_by_sis_id(self, sis_id):
        """
        Return account resource for given sis id.
        """
        return self.get_account(self._sis_id(sis_id))

    def get_sub_accounts(self, account_id, params={}):
        """
        Return list of subaccounts within the account with the passed
        canvas id.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.sub_accounts
        """
        url = ACCOUNTS_API.format(account_id) + "/sub_accounts"

        accounts = []
        for datum in self._get_paged_resource(url, params=params):
            accounts.append(CanvasAccount(data=datum))

        return accounts

    def get_sub_accounts_by_sis_id(self, sis_id):
        """
        Return list of subaccounts within the account with the passed sis id.
        """
        return self.get_sub_accounts(self._sis_id(sis_id), params={})

    def get_all_sub_accounts(self, account_id):
        """
        Return a recursive list of subaccounts within the account with
        the passed canvas id.
        """
        return self.get_sub_accounts(account_id,
                                     params={"recursive": "true"})

    def get_all_sub_accounts_by_sis_id(self, sis_id):
        """
        Return a recursive list of subaccounts within the account with
        the passed sis id.
        """
        return self.get_sub_accounts(self._sis_id(sis_id),
                                     params={"recursive": "true"})

    def update_account(self, account):
        """
        Update the passed account. Returns the updated account.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update
        """
        url = ACCOUNTS_API.format(account.account_id)
        body = {"account": {"name": account.name}}

        return CanvasAccount(data=self._put_resource(url, body))

    def update_sis_id(self, account_id, sis_account_id):
        """
        Updates the SIS ID for the account identified by the passed account ID.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.update
        """
        if account_id == self._canvas_account_id:
            raise Exception("SIS ID cannot be updated for the root account")

        url = ACCOUNTS_API.format(account_id)
        body = {"account": {"sis_account_id": sis_account_id}}

        return CanvasAccount(data=self._put_resource(url, body))

    def get_auth_settings(self, account_id):
        """
        Return the authentication settings for the passed account_id.

        https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show_sso_settings
        """
        url = ACCOUNTS_API.format(account_id) + "/sso_settings"
        return CanvasSSOSettings(data=self._get_resource(url))

    def update_auth_settings(self, account_id, auth_settings):
        """
        Update the authentication settings for the passed account_id.

        https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update_sso_settings
        """
        url = ACCOUNTS_API.format(account_id) + "/sso_settings"
        body = {"sso_settings": auth_settings.json_data()}
        return CanvasSSOSettings(data=self._put_resource(url, body))
