from uw_canvas import Canvas
from uw_canvas.models import Assignment
import dateutil.parser


class Assignments(Canvas):
    def get_assignments(self, course_id):
        """
        List assignments for a given course

        https://canvas.instructure.com/doc/api/assignments.html#method.assignments_api.index
        """
        url = "/api/v1/courses/%s/assignments" % course_id
        data = self._get_resource(url)
        assignments = []
        for assignment in data:
            assignment = self._assignment_from_json(assignment)
            assignments.append(assignment)
        return assignments

    def get_assignments_by_sis_id(self, sis_id):
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
        url = "/api/v1/courses/%s/assignments/%s" % (assignment.course_id,
                                                     assignment.assignment_id)

        data = self._put_resource(url, assignment.json_data())
        return self._assignment_from_json(data)

    def _assignment_from_json(self, data):
        assignment = Assignment()
        assignment.assignment_id = data['id']
        assignment.course_id = data['course_id']
        assignment.integration_id = data['integration_id']
        assignment.integration_data = data['integration_data']
        if 'due_at' in data and data['due_at']:
            assignment.due_at = dateutil.parser.parse(data['due_at'])
        assignment.points_possible = data['points_possible']
        assignment.grading_type = data['grading_type']
        assignment.grading_standard_id = data['grading_standard_id']
        assignment.position = data['position']
        assignment.name = data['name']
        assignment.muted = data['muted']
        assignment.html_url = data['html_url']
        return assignment
