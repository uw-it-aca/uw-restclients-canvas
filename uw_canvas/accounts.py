from uw_canvas import Canvas
from uw_canvas.models import CanvasAccount, CanvasSSOSettings


class Accounts(Canvas):
    def get_account(self, account_id):
        """
        Return account resource for given canvas account id.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.show
        """
        url = "/api/v1/accounts/%s" % account_id
        return self._account_from_json(self._get_resource(url))

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
        url = "/api/v1/accounts/%s/sub_accounts" % (account_id)

        accounts = []
        for datum in self._get_paged_resource(url, params=params):
            accounts.append(self._account_from_json(datum))

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
        url = "/api/v1/accounts/%s" % account.account_id
        body = {"account": {"name": account.name}}

        data = self._put_resource(url, body)
        return self._account_from_json(data)

    def get_auth_settings(self, account_id):
        """
        Return the authentication settings for the passed account_id.

        https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.show_sso_settings
        """
        url = '/api/v1/accounts/%s/sso_settings' % account_id

        data = self._get_resource(url)
        return self._auth_settings_from_json(data)

    def update_auth_settings(self, account_id, auth_settings):
        """
        Update the authentication settings for the passed account_id.

        https://canvas.instructure.com/doc/api/authentication_providers.html#method.account_authorization_configs.update_sso_settings
        """
        url = '/api/v1/accounts/%s/sso_settings' % account_id

        data = self._put_resource(url, auth_settings.json_data())
        return self._auth_settings_from_json(data)

    def _auth_settings_from_json(self, data):
        sso_data = data['sso_settings']
        auth_settings = CanvasSSOSettings()
        auth_settings.change_password_url = sso_data['change_password_url']
        auth_settings.login_handle_name = sso_data['login_handle_name']
        auth_settings.unknown_user_url = sso_data['unknown_user_url']
        auth_settings.auth_discovery_url = sso_data['auth_discovery_url']
        return auth_settings

    def _account_from_json(self, data):
        account = CanvasAccount()
        account.account_id = data["id"]
        account.sis_account_id = data.get("sis_account_id", None)
        account.name = data["name"]
        account.parent_account_id = data["parent_account_id"]
        account.root_account_id = data["root_account_id"]
        return account
