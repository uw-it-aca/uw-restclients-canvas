# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.roles import Roles


@fdao_canvas_override
class CanvasTestRoles(TestCase):
    def test_roles(self):
        canvas = Roles()

        roles = canvas.get_roles_in_account(12345)

        self.assertEquals(len(roles), 15, "Failed to follow Link header")

        role = roles[10]

        self.assertEquals(role.base_role_type, "AccountMembership")
        self.assertEquals(role.label, "Course Access")
        self.assertEquals(
            role.permissions.get('read_course_list').get('enabled'), True)

    def test_course_roles(self):
        canvas = Roles()

        roles = canvas.get_effective_course_roles_in_account(12345)

        self.assertEquals(len(roles), 5, "Course roles only")

        role = roles[0]
        self.assertEquals(role.base_role_type, "TeacherEnrollment")
        self.assertEquals(role.label, "Teacher")

    def test_role(self):
        canvas = Roles()

        role = canvas.get_role(12345, 999)

        self.assertEquals(role.role_id, 999)
        self.assertEquals(role.label, "Course Access")
        self.assertEquals(
            role.permissions.get('read_course_list').get('enabled'), True)

    def test_role_json_data(self):
        canvas = Roles()
        role = canvas.get_role(12345, 999)

        json_data = role.json_data()
        self.assertEqual(json_data["label"], "Course Access")
        self.assertEqual(json_data["base_role_type"], "AccountMembership")
        self.assertEqual(json_data["workflow_state"], "active")
        self.assertEqual(type(json_data["permissions"]), dict)
