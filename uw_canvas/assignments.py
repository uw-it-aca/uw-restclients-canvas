# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import Assignment

ASSIGNMENTS_API = COURSES_API + "/assignments"


class Assignments(Canvas):
    def get_assignments(self, course_id, **params):
        """
        List assignments for a given course

        https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        url = ASSIGNMENTS_API.format(course_id)
        data = self._get_paged_resource(url, params=params)
        assignments = []
        for datum in data:
            assignments.append(Assignment(data=datum))
        return assignments

    def get_assignments_by_sis_id(self, sis_id, **params):
        """
        List assignments for a given course by sid_id

        https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        return self.get_assignments(self._sis_id(sis_id, "course"))

    def update_assignment(self, assignment):
        """
        Modify an existing assignment.

        https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.update
        """
        url = ASSIGNMENTS_API.format(assignment.course_id) + "/{}".format(
            assignment.assignment_id)

        data = self._put_resource(url, {"assignment": assignment.json_data()})
        return Assignment(data=data)
