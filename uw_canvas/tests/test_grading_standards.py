from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.grading_standards import GradingStandards
import mock


@fdao_canvas_override
class CanvasTestGradingStandards(TestCase):
    def setUp(self):
        self.json_data = {
            "id": "1",
            "title": "Test Grading Standard",
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
    def test_get_grading_standards_for_course(self, mock_get):
        mock_get.return_value = [self.json_data]
        canvas = GradingStandards()

        ret = canvas.get_grading_standards_for_course("123456")
        mock_get.assert_called_with(
            '/api/v1/courses/123456/grading_standards')

        model = ret[0]
        self.assertEqual(model.grading_standard_id, self.json_data["id"])
        self.assertEqual(model.title, self.json_data["title"])
        self.assertEqual(model.context_type, self.json_data["context_type"])
        self.assertEqual(model.context_id, self.json_data["context_id"])
        self.assertEqual(model.grading_scheme,
                         self.json_data["grading_scheme"])

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
