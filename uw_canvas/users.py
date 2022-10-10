# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas, MissingAccountID
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.courses import COURSES_API
from uw_canvas.models import CanvasUser, Login

USERS_API = "/api/v1/users/{}"


class Users(Canvas):
    def get_user(self, user_id, params={}):
        """
        Returns user details.

        https://canvas.instructure.com/doc/api/users.html#method.users.api_show
        """
        url = USERS_API.format(user_id)
        return CanvasUser(data=self._get_resource(url, params=params))

    def get_user_by_sis_id(self, sis_user_id, params={}):
        """
        Returns user details for the passed user sis id.

        https://canvas.instructure.com/doc/api/users.html#method.users.api_show
        """
        return self.get_user(self._sis_id(sis_user_id, sis_field="user"),
                             params)

    def get_users_for_course(self, course_id, params={}):
        """
        Returns a list of users for the given course id.
        """
        url = COURSES_API.format(course_id) + "/users"
        data = self._get_paged_resource(url, params=params)
        users = []
        for datum in data:
            users.append(CanvasUser(data=datum))
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
            account_id = self._canvas_account_id
            if account_id is None:
                raise MissingAccountID()

        url = ACCOUNTS_API.format(account_id) + "/users"

        data = self._post_resource(url, user.post_data())
        return CanvasUser(data=data)

    def merge_users(self, user, destination_user):
        """
        Merge user into another user.

        https://canvas.instructure.com/doc/api/users.html#method.users.merge_into
        """
        url = USERS_API.format(user.user_id) + "/merge_into/{}".format(
            destination_user.user_id)
        data = self._put_resource(url)
        return CanvasUser(data=data)

    def get_user_logins(self, user_id, params={}):
        """
        Return a user's logins for the given user_id.

        https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.index
        """
        url = USERS_API.format(user_id) + "/logins"

        data = self._get_paged_resource(url, params=params)

        logins = []
        for login_data in data:
            logins.append(Login(data=login_data))

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
            account_id = self._canvas_account_id
            if account_id is None:
                raise MissingAccountID

        login_id = login.login_id
        url = ACCOUNTS_API.format(account_id) + "/logins/{}".format(login_id)

        data = self._put_resource(url, login.put_data())
        return Login(data=data)

    def delete_user_login(self, login):
        """
        Delete an existing login.

        https://canvas.instructure.com/doc/api/logins.html#method.pseudonyms.destroy
        """
        login_id = login.login_id
        url = USERS_API.format(login.user_id) + "/logins/{}".format(login_id)
        self._delete_resource(url)

    def get_user_page_views(self, user_id, start_time=None, end_time=None):
        params = {}
        if start_time is not None:
            params["start_time"] = start_time.isoformat()
        if end_time is not None:
            params["end_time"] = end_time.isoformat()

        url = USERS_API.format(user_id) + "/page_views"
        return self._get_paged_resource(url, params=params)

    def get_user_page_views_by_sis_login_id(
            self, sis_login_id, start_time=None, end_time=None):
        return self.get_user_page_views(
            self._sis_id(sis_login_id, sis_field="login"),
            start_time=start_time, end_time=end_time)
