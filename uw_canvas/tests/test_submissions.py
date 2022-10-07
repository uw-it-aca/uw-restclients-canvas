# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.submissions import Submissions
import mock


@fdao_canvas_override
class CanvasTestSubmissions(TestCase):
    def test_submissions_by_course_and_assignment(self):
        canvas = Submissions()
        submissions = canvas.get_submissions_by_course_and_assignment(
            862539, 2367793)
        self.assertEquals(len(submissions), 4, "Submission Count")

        submission = submissions[2]
        self.assertEquals(len(submission.attachments), 1, "Attachment Count")
        self.assertEquals(
            submission.attachments[0].url,
            "https://test.instructure.com/files/12345/download",
            "Attachment URL")

    def test_submissions_by_course_id(self):
        canvas = Submissions()
        submissions = canvas.get_submissions_multiple_assignments(
            False, "862539", students="all")
        self.assertEquals(len(submissions), 4, "Submission Count")

        sub = submissions[0]
        self.assertEquals(
            sub.submission_id, 12687216, "Has correct submission id")
        self.assertEquals(
            sub.grade_matches_current_submission, True,
            "Grades match current submission")
        self.assertEquals(sub.graded_at.day, 13, "Graded at datetime")
        self.assertEquals(sub.url, None, "Submitted url")

    def test_submission_by_sis_id(self):
        canvas = Submissions()
        submissions = canvas.get_submissions_multiple_assignments_by_sis_id(
            False, "2013-autumn-PHYS-248-A", students="all")
        self.assertEquals(len(submissions), 3, "Submission Count")

    @mock.patch.object(Submissions, '_get_resource_url')
    def test_get_submissions_multiple_assignments(self, mock_get):
        canvas = Submissions()
        result = canvas.get_submissions_multiple_assignments(
            False, "12345", students=["111111", "222222"])
        mock_get.assert_called_with(
            '/api/v1/courses/12345/students/submissions?student_ids[]='
            '111111&student_ids[]=222222', True, None)

        result = canvas.get_submissions_multiple_assignments(
            False, "12345", assignments=["4444444", "5555555"])
        mock_get.assert_called_with(
            '/api/v1/courses/12345/students/submissions?assignment_ids[]='
            '4444444&assignment_ids[]=5555555', True, None)

        result = canvas.get_submissions_multiple_assignments(
            True, "123456", students=["333333", "777777"],
            workflow_state="submitted")
        mock_get.assert_called_with(
            '/api/v1/sections/123456/students/submissions?student_ids[]='
            '333333&student_ids[]=777777&workflow_state=submitted',
            True, None)

    @mock.patch.object(Submissions, '_get_resource_url')
    def test_get_submissions_multiple_assignments_by_sis_id(self, mock_get):
        canvas = Submissions()
        result = canvas.get_submissions_multiple_assignments_by_sis_id(
            False, "2013-autumn-PHYS-248-A", students=["111111", "222222"])
        mock_get.assert_called_with(
            '/api/v1/courses/sis_course_id%3A2013-autumn-PHYS-248-A/'
            'students/submissions?student_ids[]=111111&student_ids[]=222222',
            True, None)

        result = canvas.get_submissions_multiple_assignments_by_sis_id(
            True, "2013-autumn-PHYS-248-AB", students=["333333", "777777"])
        mock_get.assert_called_with(
            '/api/v1/sections/sis_section_id%3A2013-autumn-PHYS-248-AB/'
            'students/submissions?student_ids[]=333333&student_ids[]=777777',
            True, None)

        result = canvas.get_submissions_multiple_assignments_by_sis_id(
            is_section=True, sis_id='2013-autumn-PHYS-248-AB',
            student_ids=['all'])
        mock_get.assert_called_with(
            '/api/v1/sections/sis_section_id%3A2013-autumn-PHYS-248-AB/'
            'students/submissions?student_ids[]=all',
            True, None)
