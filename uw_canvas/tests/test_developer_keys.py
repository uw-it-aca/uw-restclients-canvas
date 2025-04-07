# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.developer_keys import DeveloperKeys
import mock


@fdao_canvas_override
class CanvasTestDeveloperKeys(TestCase):
    def setUp(self):
        self.json_data = {
            "tool_configuration": {
                "settings": {
                    "public_jwk": {},
                    "title": "Test One",
                    "description": "First Test",
                    "target_link_uri": "http://test.edu",
                    "oidc_initiation_url": "http://test.edu",
                    "public_jwk_url": "http://test.edu/lti/jwk",
                    "scopes": [],
                    "extensions": [],
                    "custom_fields": {},
                }
            },
            "developer_key": {
                "name": "Test One Tool",
                "redirect_uris": "http://test.edu",
                "scopes": []
            }
        }

    def test_get_developer_keys(self):
        canvas = DeveloperKeys()

        keys = canvas.get_developer_keys()

        self.assertEqual(len(keys), 2, "Correct tools length")
        self.assertEqual(keys[1]['name'], "LTI Two", "Name is Correct")

    @mock.patch.object(DeveloperKeys, '_put_resource')
    def test_update_developer_key(self, mock_update):
        canvas = DeveloperKeys()
        canvas.update_developer_key("8675309", self.json_data)
        mock_update.assert_called_with(
            '/api/v1/developer_keys/8675309',
            body=self.json_data)
