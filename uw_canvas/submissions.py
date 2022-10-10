# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.sections import SECTIONS_API
from uw_canvas.models import Submission


class Submissions(Canvas):
    def get_submissions_by_course_and_assignment(
            self, course_id, assignment_id, params={}):
        """
        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
        """
        url = COURSES_API.format(course_id)
        url += "/assignments/{}/submissions".format(assignment_id)

        submissions = []
        for data in self._get_paged_resource(url, params=params):
            submissions.append(Submission(data=data))
        return submissions

    def get_submissions_multiple_assignments_by_sis_id(
            self, is_section, sis_id, students=None, assignments=None,
            **params):
        """
        List submissions for multiple assignments by course/section sis id and
        optionally student

        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        if is_section:
            return self.get_submissions_multiple_assignments(
                is_section, self._sis_id(sis_id, 'section'), students,
                assignments, **params)
        else:
            return self.get_submissions_multiple_assignments(
                is_section, self._sis_id(sis_id, 'course'), students,
                assignments, **params)

    def get_submissions_multiple_assignments(
            self, is_section, course_id, students=None, assignments=None,
            **params):
        """
        List submissions for multiple assignments by course/section id and
        optionally student

        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        api = SECTIONS_API if is_section else COURSES_API
        if students is not None:
            params['student_ids'] = students
        if assignments is not None:
            params['assignment_ids'] = assignments

        url = api.format(course_id) + "/students/submissions"
        data = self._get_paged_resource(url, params=params)
        submissions = []
        for submission in data:
            submissions.append(Submission(data=submission))
        return submissions
