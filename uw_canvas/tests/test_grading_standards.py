# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from commonconf import override_settings
from uw_canvas import MissingAccountID
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.grading_standards import GradingStandards
import mock


@fdao_canvas_override
class CanvasTestGradingStandards(TestCase):
    def setUp(self):
        self.account_json_data = {
            "id": "2",
            "title": "Test Account Grading Standard",
            "context_type": "Account",
            "context_id": "999999",
            "grading_scheme": [
                {"name": "A", "value": 0.95},
                {"name": "B", "value": 0.85},
                {"name": "C", "value": 0.75},
                {"name": "D", "value": 0.65},
            ]
        }

        self.course_json_data = {
            "id": "1",
            "title": "Test Course Grading Standard",
            "context_type": "Course",
            "context_id": "123456",
            "grading_scheme": [
                {"name": "A", "value": 0.9},
                {"name": "B", "value": 0.8},
                {"name": "C", "value": 0.7},
                {"name": "D", "value": 0.6},
            ]
        }

    @mock.patch.object(GradingStandards, '_get_resource')
    def test_get_grading_standard_for_account(self, mock_get):
        mock_get.return_value = self.account_json_data
        canvas = GradingStandards()

        model = canvas.get_grading_standard_for_account(
            "999999", "123")
        mock_get.assert_called_with(
            '/api/v1/accounts/999999/grading_standards/123')
        self.assertEqual(model.json_data(), self.account_json_data)

    @mock.patch.object(GradingStandards, '_get_resource')
    def test_find_grading_standard_for_account(self, mock_get):
        mock_get.return_value = self.account_json_data
        canvas = GradingStandards()
        model = canvas.find_grading_standard_for_account(999999, 2)
        self.assertEqual(model.json_data(), self.account_json_data)

    @override_settings(RESTCLIENTS_CANVAS_ACCOUNT_ID=None)
    def test_find_grading_standard_for_missing_root_account(self):
        canvas = GradingStandards()
        self.assertRaises(
            MissingAccountID, canvas.find_grading_standard_for_account,
            999999, 2)

    @mock.patch.object(GradingStandards, '_get_resource')
    def test_get_grading_standard_for_course(self, mock_get):
        mock_get.return_value = self.course_json_data
        canvas = GradingStandards()

        model = canvas.get_grading_standard_for_course(
            "123456", "225")
        mock_get.assert_called_with(
            '/api/v1/courses/123456/grading_standards/225')
        self.assertEqual(model.json_data(), self.course_json_data)

    @mock.patch.object(GradingStandards, '_get_resource_url')
    def test_get_grading_standards_for_course(self, mock_get):
        mock_get.return_value = [self.course_json_data]
        canvas = GradingStandards()

        ret = canvas.get_grading_standards_for_course("123456")
        mock_get.assert_called_with(
            '/api/v1/courses/123456/grading_standards', True, None)

        model = ret[0]
        self.assertEqual(
            model.grading_standard_id, self.course_json_data["id"])
        self.assertEqual(model.title, self.course_json_data["title"])
        self.assertEqual(
            model.context_type, self.course_json_data["context_type"])
        self.assertEqual(
            model.context_id, self.course_json_data["context_id"])
        self.assertEqual(
            model.grading_scheme, self.course_json_data["grading_scheme"])

    @mock.patch.object(GradingStandards, '_post_resource')
    def test_create_grading_standard_for_course(self, mock_create):
        mock_create.return_value = None
        canvas = GradingStandards()

        canvas.create_grading_standard_for_course(
            "123456", "New Grading Standard", [{"name": "A", "value": 0.9}],
            "5555555")
        mock_create.assert_called_with(
            '/api/v1/courses/123456/grading_standards', {
                'title': 'New Grading Standard',
                'grading_scheme_entry': [{"name": "A", "value": 0.9}],
                'as_user_id': '5555555'})
