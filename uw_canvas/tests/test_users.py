# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from commonconf import override_settings
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.users import Users
from uw_canvas.models import CanvasUser
from uw_canvas import MissingAccountID
from datetime import datetime
import mock


class CanvasTestUsersMissingAccount(TestCase):
    def test_create_user(self):
        canvas = Users()

        new_user = CanvasUser(
            name="J AVG USR",
            login_id="testid99",
            sis_user_id="DEB35E0A465242CF9C5CDBC108050EC0",
            email="testid99@foo.com",
            locale="en")

        self.assertRaises(MissingAccountID, canvas.create_user, new_user)


@fdao_canvas_override
class CanvasTestUsers(TestCase):
    def test_get_user(self):
        canvas = Users()
        user = canvas.get_user(188885)

        self.assertEquals(user.user_id, 188885, "Has correct user id")
        self.assertEquals(user.name, "J AVG USR", "Has correct name")
        self.assertEquals(user.short_name, "J USR", "Has correct short name")
        self.assertEquals(
            user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
            "Has correct sis id")
        self.assertEquals(user.email, "testid99@foo.edu", "Has correct email")

        user = canvas.get_user_by_sis_id("DEB35E0A465242CF9C5CDBC108050EC0")

        self.assertEquals(user.user_id, 188885, "Has correct user id")
        self.assertEquals(user.name, "J AVG USR", "Has correct name")
        self.assertEquals(user.short_name, "J USR", "Has correct short name")
        self.assertEquals(
            user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
            "Has correct sis id")
        self.assertEquals(user.email, "testid99@foo.edu", "Has correct email")
        self.assertEquals(user.avatar_url, (
            "https://en.gravatar.com/avatar/d8cb8c8cd40ddf0c"
            "d05241443a591868?s=80&r=g"), "Has correct avatar url")

    @mock.patch.object(Users, '_get_resource')
    def test_get_user_params(self, mock_get):
        canvas = Users()
        params = {'include': 'last_login'}

        user = canvas.get_user(188885, params)
        mock_get.assert_called_with('/api/v1/users/188885',
                                    params={'include': 'last_login'})

        user = canvas.get_user_by_sis_id(
            "DEB35E0A465242CF9C5CDBC108050EC0", params)
        mock_get.assert_called_with(
            '/api/v1/users/sis_user_id%3ADEB35E0A465242CF9C5CDBC108050EC0',
            params={'include': 'last_login'})

    def test_json_data(self):
        canvas = Users()
        user = canvas.get_user(188885)

        self.assertEqual(user.json_data(), {
            'avatar_url': (
                'https://en.gravatar.com/avatar/d8cb8c8cd40ddf0c'
                'd05241443a591868?s=80&r=g'),
            'bio': None,
            'email': 'testid99@foo.edu',
            'enrollments': [],
            'id': 188885,
            'last_login': '2013-02-20T14:45:27+00:00',
            'locale': None,
            'login_id': 'testid99',
            'name': 'J AVG USR',
            'short_name': 'J USR',
            'sis_user_id': 'DEB35E0A465242CF9C5CDBC108050EC0',
            'sortable_name': 'USR, J AVG',
            'time_zone': None})

    @mock.patch.object(Users, '_post_resource')
    def test_create_user(self, mock_create):
        canvas = Users()

        new_user = CanvasUser(
            name="J AVG USR",
            login_id="testid99",
            sis_user_id="DEB35E0A465242CF9C5CDBC108050EC0",
            email="testid99@foo.com",
            locale="en")

        account_id = 88888
        canvas.create_user(new_user, account_id)
        mock_create.assert_called_with('/api/v1/accounts/88888/users', {
            'communication_channel': {
                'type': 'email',
                'skip_confirmation': True,
                'address': 'testid99@foo.com'
            },
            'user': {
                'locale': 'en',
                'sortable_name': None,
                'name': 'J AVG USR',
                'short_name': None,
                'time_zone': None
            },
            'pseudonym': {
                'sis_user_id': 'DEB35E0A465242CF9C5CDBC108050EC0',
                'send_confirmation': False,
                'unique_id': 'testid99'
            }
        })

    @mock.patch.object(Users, '_put_resource')
    def test_merge_users(self, mock_merge):
        canvas = Users()

        user = CanvasUser(
            user_id=12345,
            name="J AVG USR",
            login_id="testid99",
            sis_user_id="DEB35E0A465242CF9C5CDBC108050EC0",
            email="testid99@foo.com",
            locale="en")

        destination_user = CanvasUser(
            user_id=56789,
            name="J AVG USR",
            login_id="javerage",
            sis_user_id="15AE3883B6EC44C349E04E5FE089ABEB",
            email="javerage@example.edu",
            locale="en")

        canvas.merge_users(user, destination_user)
        mock_merge.assert_called_with('/api/v1/users/12345/merge_into/56789')

    def test_get_users_for_course_id(self):
        canvas = Users()

        users = canvas.get_users_for_course("862539", params={
            "search_term": "jav", "include": ["enrollments"]})

        self.assertEquals(len(users), 3, "Found 3 canvas users")

        user = users[0]
        self.assertEquals(user.login_id, "javerage", "Login ID")
        self.assertEquals(
            user.sis_user_id, "15AE3883B6EC44C349E04E5FE089ABEB",
            "SIS User ID")
        self.assertEquals(user.name, "JAMES AVERAGE", "Name")
        self.assertEquals(
            user.sortable_name, "AVERAGE, JAMES", "Sortable Name")
        enrollment = user.enrollments[0]
        self.assertEquals(enrollment.sis_course_id, "2015-summer-TRAIN-100-A")
        self.assertEquals(enrollment.role, "Librarian", "Role")
        self.assertEquals(
            enrollment.base_role_type, "DesignerEnrollment", "Base Role Type")

    def test_get_logins(self):
        canvas = Users()

        user_id = 188885
        sis_user_id = "DEB35E0A465242CF9C5CDBC108050EC0"
        logins = canvas.get_user_logins(user_id)

        self.assertEquals(len(logins), 2, "Has correct login count")

        login = logins[0]
        self.assertEquals(login.user_id, user_id, "Has correct user id")
        self.assertEquals(login.login_id, 100, "Has correct login_id")
        self.assertEquals(login.sis_user_id, sis_user_id, "Has correct sis id")
        self.assertEquals(login.unique_id, "testid99", "Has correct unique id")

        logins = canvas.get_user_logins_by_sis_id(sis_user_id)

        self.assertEquals(len(logins), 2, "Has correct login count")

        login = logins[0]
        self.assertEquals(login.user_id, user_id, "Has correct user id")
        self.assertEquals(login.login_id, 100, "Has correct login_id")
        self.assertEquals(login.sis_user_id, sis_user_id, "Has correct sis id")
        self.assertEquals(login.unique_id, "testid99", "Has correct unique id")

    @mock.patch.object(Users, '_put_resource')
    def test_update_login(self, mock_update):
        canvas = Users()

        user_id = 188885
        logins = canvas.get_user_logins(user_id)

        login = logins[0]
        login.unique_id = "testid99new"
        login.sis_user_id = ""

        canvas.update_user_login(login, account_id=12345)
        mock_update.assert_called_with(
            '/api/v1/accounts/12345/logins/100',
            {'login': {'sis_user_id': '', 'unique_id': 'testid99new'}})

        with override_settings(RESTCLIENTS_CANVAS_ACCOUNT_ID=None):
            canvas = Users()
            self.assertRaises(
                MissingAccountID, canvas.update_user_login, login)

    @mock.patch.object(Users, '_delete_resource')
    def test_delete_login(self, mock_delete):
        canvas = Users()

        user_id = 188885
        logins = canvas.get_user_logins(user_id)
        login = logins[0]

        canvas.delete_user_login(login)
        mock_delete.assert_called_with('/api/v1/users/188885/logins/100')

    @mock.patch.object(Users, '_get_resource_url')
    def test_get_page_views(self, mock_get):
        canvas = Users()
        user_id = 11111

        ret = canvas.get_user_page_views(user_id)
        mock_get.assert_called_with(
            '/api/v1/users/11111/page_views', True, None)

        start = datetime(2015, 1, 1)
        ret = canvas.get_user_page_views(user_id, start_time=start)
        mock_get.assert_called_with(
            '/api/v1/users/11111/page_views?'
            'start_time=2015-01-01T00%3A00%3A00', True, None)

        end = datetime(2017, 1, 1)
        ret = canvas.get_user_page_views(
            user_id, start_time=start, end_time=end)
        mock_get.assert_called_with(
            '/api/v1/users/11111/page_views?'
            'end_time=2017-01-01T00%3A00%3A00&'
            'start_time=2015-01-01T00%3A00%3A00', True, None)

    @mock.patch.object(Users, '_get_resource_url')
    def test_get_page_views_by_sis_login_id(self, mock_get):
        canvas = Users()
        login_id = 'javerage'

        ret = canvas.get_user_page_views_by_sis_login_id(login_id)
        mock_get.assert_called_with(
            '/api/v1/users/sis_login_id%3Ajaverage/page_views', True, None)

        start = datetime(2015, 1, 1)
        ret = canvas.get_user_page_views_by_sis_login_id(
            login_id, start_time=start)
        mock_get.assert_called_with(
            '/api/v1/users/sis_login_id%3Ajaverage/page_views?'
            'start_time=2015-01-01T00%3A00%3A00', True, None)

        end = datetime(2017, 1, 1)
        ret = canvas.get_user_page_views_by_sis_login_id(
            login_id, start_time=start, end_time=end)
        mock_get.assert_called_with(
            '/api/v1/users/sis_login_id%3Ajaverage/page_views?'
            'end_time=2017-01-01T00%3A00%3A00&'
            'start_time=2015-01-01T00%3A00%3A00', True, None)
