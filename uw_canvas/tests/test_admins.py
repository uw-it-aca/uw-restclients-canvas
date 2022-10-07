# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.admins import Admins
import mock


@fdao_canvas_override
class CanvasTestAdmins(TestCase):
    def test_admins(self):
        canvas = Admins()

        admins = canvas.get_admins_by_sis_id('uwcourse:seattle:nursing:nurs')

        self.assertEquals(len(admins), 11, "Failed to follow Link header")

        admin = admins[10]

        self.assertEquals(admin.role, 'AccountAdmin', "Has proper role")
        self.assertEquals(admin.user.user_id, 1111, "Has proper id")

    @mock.patch.object(Admins, '_post_resource')
    def test_create_admin(self, mock_post):
        canvas = Admins()

        canvas.create_admin_by_sis_id(
            'uwcourse:seattle:nursing:nurs', 1111, 'AccountAdmin')
        mock_post.assert_called_with((
            '/api/v1/accounts/sis_account_id%3Auwcourse%3Aseattle'
            '%3Anursing%3Anurs/admins'), {
                'role': 'AccountAdmin',
                'send_confirmation': False,
                'user_id': '1111'
            })

    @mock.patch.object(Admins, '_delete_resource')
    def test_delete_admin(self, mock_delete):
        canvas = Admins()

        canvas.delete_admin_by_sis_id(
            'uwcourse:seattle:nursing:nurs', 1111, 'AccountAdmin')
        mock_delete.assert_called_with((
            '/api/v1/accounts/sis_account_id%3Auwcourse%3Aseattle%3Anursing'
            '%3Anurs/admins/1111?role=AccountAdmin'))
