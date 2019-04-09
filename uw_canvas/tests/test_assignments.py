from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.assignments import Assignments
from uw_canvas.models import Assignment
import mock


@fdao_canvas_override
class CanvasTestAssignments(TestCase):
    def test_assignments_by_course_id(self):
        canvas = Assignments()
        assignments = canvas.get_assignments("862539")
        assignment = assignments[0]
        self.assertEquals(assignment.name, "Assignment 1", "Assignment name")
        self.assertEquals(assignment.muted, False, "Assignment isn't muted")
        self.assertEquals(
            assignment.published, True, "Assignment is published")
        self.assertEquals(assignment.due_at.day, 1, "Due date")
        self.assertEquals(assignment.grading_type, "points", "Grading type")
        self.assertEquals(
            assignment.grading_standard_id, None, "Grading Standard ID")
        self.assertEquals(
            assignment.turnitin_enabled, False, "turnitin enabled")
        self.assertEquals(
            assignment.vericite_enabled, True, "vericite enabled")
        self.assertEquals(assignment.has_submissions, True, "has_submissions")
        self.assertEquals(
            assignment.submission_types, ['online_text_entry', 'online_url'])

    def test_assignment_by_course_sis_id(self):
        canvas = Assignments()
        assignments = canvas.get_assignments_by_sis_id(
            "2013-autumn-PHYS-248-A")
        self.assertEquals(len(assignments), 2, "Assignment Count")

    def test_assignment_act_as(self):
        canvas = Assignments(as_user="730FA4DCAE3411D689DA0004AC494FFE")
        assignments = canvas.get_assignments_by_sis_id(
            "2013-autumn-PHYS-248-A")
        self.assertEquals(len(assignments), 2, "Assignment Count")

    @mock.patch.object(Assignments, '_put_resource')
    def test_update_assignment(self, mock_update):
        mock_update.return_value = None
        canvas = Assignments()

        assignments = canvas.get_assignments("862539")
        assignment = assignments[0]

        canvas.update_assignment(assignment)
        mock_update.assert_called_with(
            '/api/v1/courses/862539/assignments/2367793', {
                'assignment': {'integration_id': '', 'integration_data': ''}})

    def test_json_data(self):
        canvas = Assignments()

        assignments = canvas.get_assignments_by_sis_id(
            "2013-autumn-PHYS-248-A")

        assignment = assignments[0]
        data = assignment.json_data()["assignment"]
        self.assertEquals(
            'external_tool' in assignment.submission_types, False)
        self.assertEquals('external_tool_tag_attributes' in data, False)

        assignment = assignments[1]
        data = assignment.json_data()["assignment"]
        self.assertEquals('external_tool' in assignment.submission_types, True)
        self.assertEquals('external_tool_tag_attributes' in data, True)

    def test_due_at_none(self):
        data = {
                "id": "id",
                "course_id": "cid",
                "integration_id": "X",
                "integration_data": "data",
                "points_possible": "data",
                "grading_type": "data",
                "grading_standard_id": "data",
                "position": "data",
                "name": "data",
                "muted": "data",
                "published": "data",
                "has_submitted_submissions": "data",
                "html_url": "data",
                "due_at": None
                }

        assignment = Assignment(data=data)
