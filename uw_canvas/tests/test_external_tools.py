# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.external_tools import ExternalTools
import mock


@fdao_canvas_override
class CanvasTestExternalTools(TestCase):
    def setUp(self):
        self.json_data = {
            "name": "Test LTI",
            "consumer_key": "00000000",
            "privacy_level": "public",
            "url": "https://test.edu/lti",
        }

    def test_get_external_tools_in_account(self):
        canvas = ExternalTools()

        tools = canvas.get_external_tools_in_account('12345')

        self.assertEquals(len(tools), 12, "Correct tools length")
        self.assertEquals(tools[10]['name'], "Tool", "Name is Correct")

    def test_get_external_tools_in_course_by_sis_id(self):
        canvas = ExternalTools()

        tools = canvas.get_external_tools_in_course_by_sis_id(
            '2015-autumn-UWBW-301-A')

        self.assertEquals(len(tools), 2, "Correct tools length")
        self.assertEquals(
            tools[1]['name'], 'Course Tool', "Has correct tool name")

    def test_get_sessionless_launch_from_account_sis_id(self):
        canvas = ExternalTools()

        launch = canvas.get_sessionless_launch_url_from_account(
            '54321', '12345')

        self.assertEquals(launch['id'], 54321, "Has correct tool id")

    def test_get_sessionless_launch_from_course_sis_id(self):
        canvas = ExternalTools()

        launch = canvas.get_sessionless_launch_url_from_course_sis_id(
            '54321', '2015-autumn-UWBW-301-A')

        self.assertEquals(launch['id'], 54321, "Has correct tool id")

    @mock.patch.object(ExternalTools, '_post_resource')
    def test_create_external_tool_in_course(self, mock_create):
        canvas = ExternalTools()
        canvas.create_external_tool_in_course("123456", self.json_data)
        mock_create.assert_called_with(
            '/api/v1/courses/123456/external_tools', body=self.json_data)

    @mock.patch.object(ExternalTools, '_post_resource')
    def test_create_external_tool_in_account(self, mock_create):
        canvas = ExternalTools()
        canvas.create_external_tool_in_account("11111", self.json_data)
        mock_create.assert_called_with(
            '/api/v1/accounts/11111/external_tools', body=self.json_data)

    @mock.patch.object(ExternalTools, '_put_resource')
    def test_update_external_tool_in_course(self, mock_update):
        canvas = ExternalTools()
        canvas.update_external_tool_in_course(
            "123456", "222222", self.json_data)
        mock_update.assert_called_with(
            '/api/v1/courses/123456/external_tools/222222',
            body=self.json_data)

    @mock.patch.object(ExternalTools, '_put_resource')
    def test_update_external_tool_in_account(self, mock_update):
        canvas = ExternalTools()
        canvas.update_external_tool_in_account(
            "11111", "222222", self.json_data)
        mock_update.assert_called_with(
            '/api/v1/accounts/11111/external_tools/222222',
            body=self.json_data)

    @mock.patch.object(ExternalTools, '_delete_resource')
    def test_delete_external_tool_in_course(self, mock_delete):
        canvas = ExternalTools()
        canvas.delete_external_tool_in_course("123456", "222222")
        mock_delete.assert_called_with(
            '/api/v1/courses/123456/external_tools/222222')

    @mock.patch.object(ExternalTools, '_delete_resource')
    def test_delete_external_tool_in_account(self, mock_delete):
        canvas = ExternalTools()
        canvas.delete_external_tool_in_account("11111", "222222")
        mock_delete.assert_called_with(
            '/api/v1/accounts/11111/external_tools/222222')
