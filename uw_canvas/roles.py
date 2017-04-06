from uw_canvas import Canvas
from uw_canvas.models import CanvasRole, CanvasAccount
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class Roles(Canvas):
    def get_roles_in_account(self, account_id, params={}):
        """
        List the roles for an account, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.api_index
        """
        url = "/api/v1/accounts/%s/roles" % (account_id)

        roles = []
        for datum in self._get_resource(url, params=params):
            roles.append(self._role_from_json(datum))
        return roles

    def get_roles_by_account_sis_id(self, account_sis_id, params={}):
        """
        List the roles for an account, for the passed account SIS ID.
        """
        return self.get_roles_in_account(self._sis_id(account_sis_id,
                                                      sis_field="account"),
                                         params)

    def get_effective_course_roles_in_account(self, account_id):
        """
        List all course roles available to an account, for the passed Canvas
        account ID, including course roles inherited from parent accounts.
        """
        course_roles = []
        params = {"show_inherited": "1"}
        for role in self.get_roles_in_account(account_id, params):
            if role.base_role_type != "AccountMembership":
                course_roles.append(role)
        return course_roles

    def get_role(self, account_id, role_id):
        """
        Get information about a single role, for the passed Canvas account ID.

        https://canvas.instructure.com/doc/api/roles.html#method.role_overrides.show
        """
        url = "/api/v1/accounts/%s/roles/%s" % (account_id, role_id)
        return self._role_from_json(self._get_resource(url))

    def get_role_by_account_sis_id(self, account_sis_id, role_id):
        """
        Get information about a single role, for the passed account SIS ID.
        """
        return self.get_role(self._sis_id(account_sis_id, sis_field="account"),
                             role_id)

    def _role_from_json(self, data):
        role = CanvasRole()
        role.role_id = data["id"]
        role.label = data["label"]
        role.base_role_type = data["base_role_type"]
        role.workflow_state = data["workflow_state"]
        role.permissions = data.get("permissions", {})
        if "account" in data:
            role.account = CanvasAccount(data["account"])
        return role
