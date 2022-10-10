# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.models import CanvasRole
from urllib.parse import quote


class Roles(Canvas):
    def get_roles_in_account(self, account_id, params={}):
        """
        List the roles for an account, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index
        """
        url = ACCOUNTS_API.format(account_id) + "/roles"

        roles = []
        for datum in self._get_paged_resource(url, params=params):
            roles.append(CanvasRole(data=datum))
        return roles

    def get_roles_by_account_sis_id(self, account_sis_id, params={}):
        """
        List the roles for an account, for the passed account SIS ID.
        """
        return self.get_roles_in_account(self._sis_id(account_sis_id,
                                                      sis_field="account"),
                                         params)

    def get_effective_course_roles_in_account(self, account_id, params={}):
        """
        List all course roles available to an account, for the passed Canvas
        account ID, including course roles inherited from parent accounts.
        """
        course_roles = []
        params["show_inherited"] = "1"
        if "per_page" not in params:
            params["per_page"] = 100
        for role in self.get_roles_in_account(account_id, params):
            if role.base_role_type != "AccountMembership":
                course_roles.append(role)
        return course_roles

    def get_role(self, account_id, role_id):
        """
        Get information about a single role, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show
        """
        url = ACCOUNTS_API.format(account_id) + "/roles/{}".format(role_id)
        return CanvasRole(data=self._get_resource(url))

    def get_role_by_account_sis_id(self, account_sis_id, role_id):
        """
        Get information about a single role, for the passed account SIS ID.
        """
        return self.get_role(self._sis_id(account_sis_id, sis_field="account"),
                             role_id)
