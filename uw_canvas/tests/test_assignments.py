# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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
        self.assertEqual(assignment.name, "Assignment 1", "Assignment name")
        self.assertEqual(
            assignment.published, True, "Assignment is published")
        self.assertEqual(assignment.due_at.day, 1, "Due date")
        self.assertEqual(assignment.grading_type, "points", "Grading type")
        self.assertEqual(
            assignment.grading_standard_id, None, "Grading Standard ID")
        self.assertEqual(
            assignment.turnitin_enabled, False, "turnitin enabled")
        self.assertEqual(
            assignment.vericite_enabled, True, "vericite enabled")
        self.assertEqual(assignment.has_submissions, True, "has_submissions")
        self.assertEqual(
            assignment.submission_types, ['online_text_entry', 'online_url'])

    def test_assignment_by_course_sis_id(self):
        canvas = Assignments()
        assignments = canvas.get_assignments_by_sis_id(
            "2013-autumn-PHYS-248-A")
        self.assertEqual(len(assignments), 2, "Assignment Count")

    def test_assignment_act_as(self):
        canvas = Assignments(as_user="730FA4DCAE3411D689DA0004AC494FFE")
        assignments = canvas.get_assignments_by_sis_id(
            "2013-autumn-PHYS-248-A")
        self.assertEqual(len(assignments), 2, "Assignment Count")

    @mock.patch.object(Assignments, '_get_resource_url')
    def test_assignment_params(self, mock_get):
        canvas = Assignments()
        result = canvas.get_assignments("862539", include=['submission'])
        mock_get.assert_called_with(
            "/api/v1/courses/862539/assignments?include[]=submission",
            True, None)

    @mock.patch.object(Assignments, '_put_resource')
    def test_update_assignment(self, mock_update):
        mock_update.return_value = None
        canvas = Assignments()

        assignments = canvas.get_assignments("862539")
        assignment = assignments[0]

        canvas.update_assignment(assignment)
        mock_update.assert_called_with(
            '/api/v1/courses/862539/assignments/2367793', {
                'assignment': assignment.json_data()})

    def test_json_data(self):
        canvas = Assignments()

        assignments = canvas.get_assignments_by_sis_id(
            "2013-autumn-PHYS-248-A")

        assignment = assignments[0]
        data = assignment.json_data()
        self.assertEqual(assignment.assignment_id, 2367793)
        self.assertEqual(assignment.points_possible, 1000000000)
        self.assertFalse('external_tool' in assignment.submission_types)
        self.assertFalse('external_tool_tag_attributes' in data)

        assignment = assignments[1]
        data = assignment.json_data()
        self.assertEqual(assignment.assignment_id, 2367794)
        self.assertEqual(assignment.points_possible, 123)
        self.assertTrue('external_tool' in assignment.submission_types)
        self.assertTrue('external_tool_tag_attributes' in data)

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
                "published": "data",
                "has_submitted_submissions": "data",
                "html_url": "data",
                "due_at": None
                }
        assignment = Assignment(data=data)
        self.assertEqual(assignment.due_at, None)
