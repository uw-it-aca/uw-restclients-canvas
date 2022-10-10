# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.models import CanvasAdmin
from urllib.parse import quote, unquote

ADMINS_API = "/api/v1/accounts/{}/admins"


class Admins(Canvas):
    def get_admins(self, account_id, params={}):
        """
        Return a list of the admins in the account.

        https://canvas.instructure.com/doc/api/admins.html#method.admins.index
        """
        url = ADMINS_API.format(account_id)

        admins = []
        for data in self._get_paged_resource(url, params=params):
            admins.append(CanvasAdmin(data=data))
        return admins

    def get_admins_by_sis_id(self, sis_account_id):
        """
        Return a list of the admins in the account by sis id.
        """
        return self.get_admins(self._sis_id(sis_account_id))

    def create_admin(self, account_id, user_id, role):
        """
        Flag an existing user as an admin within the account.

        https://canvas.instructure.com/doc/api/admins.html#method.admins.create
        """
        url = ADMINS_API.format(account_id)
        body = {"user_id": unquote(str(user_id)),
                "role": role,
                "send_confirmation": False}

        return CanvasAdmin(data=self._post_resource(url, body))

    def create_admin_by_sis_id(self, sis_account_id, user_id, role):
        """
        Flag an existing user as an admin within the account sis id.
        """
        return self.create_admin(self._sis_id(sis_account_id), user_id, role)

    def delete_admin(self, account_id, user_id, role):
        """
        Remove an account admin role from a user.

        https://canvas.instructure.com/doc/api/admins.html#method.admins.destroy
        """
        url = ADMINS_API.format(account_id) + "/{}?role={}".format(
            user_id, quote(role))

        response = self._delete_resource(url)
        return True

    def delete_admin_by_sis_id(self, sis_account_id, user_id, role):
        """
        Remove an account admin role from a user for the account sis id.
        """
        return self.delete_admin(self._sis_id(sis_account_id), user_id, role)
