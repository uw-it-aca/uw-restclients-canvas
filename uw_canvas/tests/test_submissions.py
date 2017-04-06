from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.submissions import Submissions


@fdao_canvas_override
class CanvasTestSubmissions(TestCase):
    def test_submissions_by_course_id(self):
        canvas = Submissions()
        submissions = canvas.get_submissions_multiple_assignments(False, "862539", "all")
        self.assertEquals(len(submissions), 3, "Submission Count")

        sub = submissions[0]
        self.assertEquals(sub.submission_id, 12687216, "Has correct submission id")
        self.assertEquals(sub.grade_matches_current_submission, True, "Grades match current submission")
        self.assertEquals(sub.graded_at.day, 13, "Graded at datetime")
        self.assertEquals(sub.url, None, "Submitted url")

    def test_submission_by_sis_id(self):
        canvas = Submissions()
        submissions = canvas.get_submissions_multiple_assignments_by_sis_id(False, "2013-autumn-PHYS-248-A", "all")
        self.assertEquals(len(submissions), 3, "Submission Count")
