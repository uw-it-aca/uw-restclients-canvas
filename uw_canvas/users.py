from uw_canvas import Canvas
from uw_canvas.enrollments import Enrollments
from uw_canvas.models import CanvasUser, Login
from commonconf import settings


class Users(Canvas):
    def get_user(self, user_id):
        """
        Returns user profile data.

        https://canvas.instructure.com/doc/api/users.html#method.profile.settings
        """
        url = "/api/v1/users/%s/profile" % user_id
        return self._user_from_json(self._get_resource(url))

    def get_user_by_sis_id(self, sis_user_id):
        """
        Returns user profile data for the passed user sis id.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.users
        """
        return self.get_user(self._sis_id(sis_user_id, sis_field="user"))

    def get_users_for_course(self, course_id, params={}):
        """
        Returns a list of users for the given course id.
        """
        url = "/api/v1/courses/%s/users" % course_id
        data = self._get_paged_resource(url, params=params)
        users = []
        for datum in data:
            users.append(self._user_from_json(datum))
        return users

    def get_users_for_sis_course_id(self, sis_course_id, params={}):
        """
        Returns a list of users for the given sis course id.
        """
        return self.get_users_for_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def create_user(self, user, account_id=None):
        """
        Create and return a new user and pseudonym for an account.

        https://canvas.instructure.com/doc/api/users.html#method.users.create
        """
        if account_id is None:
            account_id = settings.RESTCLIENTS_CANVAS_ACCOUNT_ID

        url = "/api/v1/accounts/%s/users" % account_id

        data = self._post_resource(url, user.post_data())
        return self._user_from_json(data)

    def get_user_logins(self, user_id, params={}):
        """
        Return a user's logins for the given user_id.

        https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index
        """
        url = "/api/v1/users/%s/logins" % user_id

        data = self._get_paged_resource(url, params=params)

        logins = []
        for login_data in data:
            logins.append(self._login_from_json(login_data))

        return logins

    def get_user_logins_by_sis_id(self, sis_user_id):
        """
        Returns user login data for the passed user sis id.
        """
        return self.get_user_logins(self._sis_id(sis_user_id,
                                                 sis_field="user"))

    def update_user_login(self, login, account_id=None):
        """
        Update an existing login for a user in the given account.

        https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.update
        """
        if account_id is None:
            account_id = settings.RESTCLIENTS_CANVAS_ACCOUNT_ID

        url = "/api/v1/accounts/%s/logins/%s" % (account_id, login.login_id)

        data = self._put_resource(url, login.put_data())
        return self._login_from_json(data)

    def _user_from_json(self, data):
        user = CanvasUser()
        user.user_id = data["id"]
        user.name = data["name"]
        user.short_name = data["short_name"] if "short_name" in data else None
        user.sortable_name = data["sortable_name"] if (
            "sortable_name" in data) else None
        user.login_id = data["login_id"] if "login_id" in data else None
        user.sis_user_id = data["sis_user_id"] if (
            "sis_user_id" in data) else None
        user.email = data["email"] if "email" in data else None
        user.time_zone = data["time_zone"] if "time_zone" in data else None
        user.locale = data["locale"] if "locale" in data else None
        user.avatar_url = data["avatar_url"] if "avatar_url" in data else None
        if "enrollments" in data:
            enrollments = Enrollments()
            user.enrollments = []
            for enr_datum in data["enrollments"]:
                user.enrollments.append(
                    enrollments._enrollment_from_json(enr_datum))
        return user

    def _login_from_json(self, data):
        login = Login()
        login.login_id = data["id"]
        login.account_id = data["account_id"]
        login.sis_user_id = data["sis_user_id"] if (
            "sis_user_id" in data) else None
        login.unique_id = data["unique_id"]
        login.user_id = data["user_id"]
        return login
