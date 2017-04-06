from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.assignments import Assignments


@fdao_canvas_override
class CanvasTestAssignments(TestCase):
    def test_assignments_by_course_id(self):
        canvas = Assignments()
        assignments = canvas.get_assignments("862539")
        assignment = assignments[0]
        self.assertEquals(assignment.name, "Assignment 1", "Assignment name")
        self.assertEquals(assignment.muted, False, "Assignment isn't muted")
        self.assertEquals(assignment.due_at.day, 1, "Due date")
        self.assertEquals(assignment.grading_type, "points", "Grading type")
        self.assertEquals(assignment.grading_standard_id, None, "Grading Standard ID")

    def test_assignment_by_course_sis_id(self):
        canvas = Assignments()
        assignments = canvas.get_assignments_by_sis_id("2013-autumn-PHYS-248-A")
        self.assertEquals(len(assignments), 2, "Assignment Count")

    def test_assignment_act_as(self):
        canvas = Assignments(as_user="730FA4DCAE3411D689DA0004AC494FFE")
        assignments = canvas.get_assignments_by_sis_id("2013-autumn-PHYS-248-A")
        self.assertEquals(len(assignments), 2, "Assignment Count")

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
                "html_url": "data",
                "due_at": None
                }

        assignment = Assignments()._assignment_from_json(data)
