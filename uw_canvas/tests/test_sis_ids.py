from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.models import CanvasEnrollment, CanvasCourse


@fdao_canvas_override
class CanvasBadSISIDs(TestCase):
    def test_enrollment(self):
        enrollment = CanvasEnrollment()
        enrollment.sis_id = "2013-winter-CHEM-121"
        sws_id = enrollment.sws_course_id()

        self.assertEquals(sws_id, None, "Invalid SIS ID leads to an sws_id of None")

    def test_course(self):
        course = CanvasCourse()
        course.sis_id = "2013-winter-CHEM-121"
        sws_id = course.sws_course_id()

        self.assertEquals(sws_id, None, "Invalid SIS ID leads to an sws_id of None")
