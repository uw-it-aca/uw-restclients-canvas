# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.lti_registrations import LTIRegistrations
from restclients_core.exceptions import DataFailureException
import mock


@fdao_canvas_override
class CanvasTestLTIRegistrations(TestCase):
    def setUp(self):
        self.json_data = {
            "name": "LTI One Update",
            "configuration": {
                "title": "LTI One (1)",
                "target_link_uri": "https://example.edu/launch",
            }
        }

    def test_get_lti_registrations(self):
        canvas = LTIRegistrations()

        regs = canvas.get_registrations(
            params={'include': 'overlaid_configuration'})

        self.assertEqual(len(regs), 2, "Correct tools length")
        self.assertEqual(regs[1]['name'], "LTI Two", "Name is Correct")

    def test_get_lti_registration_by_id(self):
        canvas = LTIRegistrations()

        reg = canvas.get_registration_by_id(
            1, params={'include': 'overlaid_configuration'})

        self.assertEqual(reg.get('id'), 1, "Correct registration ID")

        with self.assertRaises(DataFailureException):
            canvas.get_registration_by_id(9999)

    @mock.patch.object(LTIRegistrations, '_put_resource')
    def test_update_lti_registration(self, mock_update):
        canvas = LTIRegistrations()
        canvas.update_registration(1, self.json_data)
        mock_update.assert_called_with(
            '/api/v1/accounts/12345/lti_registrations/1',
            body=self.json_data)
