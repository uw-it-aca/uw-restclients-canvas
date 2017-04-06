from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.users import Users
from uw_canvas.models import CanvasUser
import mock


@fdao_canvas_override
class CanvasTestUsers(TestCase):
    def test_get_user(self):
        canvas = Users()

        user = canvas.get_user(188885)

        self.assertEquals(user.user_id, 188885, "Has correct user id")
        self.assertEquals(user.name, "J AVG USR", "Has correct name")
        self.assertEquals(user.short_name, None, "Has correct short name")
        self.assertEquals(user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
                          "Has correct sis id")
        self.assertEquals(user.email, "testid99@foo.com", "Has correct email")

        user = canvas.get_user_by_sis_id("DEB35E0A465242CF9C5CDBC108050EC0")

        self.assertEquals(user.user_id, 188885, "Has correct user id")
        self.assertEquals(user.name, "J AVG USR", "Has correct name")
        self.assertEquals(user.short_name, None, "Has correct short name")
        self.assertEquals(user.sis_user_id, "DEB35E0A465242CF9C5CDBC108050EC0",
                          "Has correct sis id")
        self.assertEquals(user.email, "testid99@foo.com", "Has correct email")
        self.assertEquals(user.avatar_url, "https://en.gravatar.com/avatar/d8cb8c8cd40ddf0cd05241443a591868?s=80&r=g", "Has correct avatar url")

    @mock.patch.object(Users, '_post_resource')
    def test_create_user(self, mock_create):
        canvas = Users()

        new_user = CanvasUser(name="J AVG USR",
            login_id="testid99",
            sis_user_id="DEB35E0A465242CF9C5CDBC108050EC0",
            email="testid99@foo.com",
            locale="en")

        account_id = 88888
        canvas.create_user(new_user, account_id)
        mock_create.assert_called_with(
            '/api/v1/accounts/88888/users',
            {'communication_channel': {'type': 'email', 'skip_confirmation': True, 'address': 'testid99@foo.com'}, 'user': {'locale': 'en', 'sortable_name': None, 'name': 'J AVG USR', 'short_name': None, 'time_zone': None}, 'pseudonym': {'sis_user_id': 'DEB35E0A465242CF9C5CDBC108050EC0', 'send_confirmation': False, 'unique_id': 'testid99'}})

    def test_get_users_for_course_id(self):
        canvas = Users()

        users = canvas.get_users_for_course("862539",
            params={"search_term": "jav", "include": ["enrollments"]})

        self.assertEquals(len(users), 3, "Found 3 canvas users")

        user = users[0]
        self.assertEquals(user.login_id, "javerage", "Login ID")
        self.assertEquals(user.sis_user_id, "15AE3883B6EC44C349E04E5FE089ABEB", "SIS User ID")
        self.assertEquals(user.name, "JAMES AVERAGE", "Name")
        self.assertEquals(user.sortable_name, "AVERAGE, JAMES", "Sortable Name")
        enrollment = user.enrollments[0]
        self.assertEquals(enrollment.sis_course_id, "2015-summer-TRAIN-100-A")
        self.assertEquals(enrollment.role, "DesignerEnrollment", "Role")

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
