from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.courses import Courses
from uw_canvas.models import CanvasCourse
import mock


@fdao_canvas_override
class CanvasTestCourses(TestCase):
    def test_course(self):
        canvas = Courses()

        course = canvas.get_course(149650)

        self.assertEquals(course.course_id, 149650, "Has proper course id")
        self.assertEquals(
            course.course_url, "https://canvas.uw.edu/courses/149650",
            "Has proper course url")
        self.assertEquals(course.sis_course_id, "2013-spring-PHYS-121-A")
        self.assertEquals(course.sws_course_id(), "2013,spring,PHYS,121/A")
        self.assertEquals(course.sws_instructor_regid(), None)
        self.assertEquals(course.is_academic_sis_id(), True)
        self.assertEquals(course.account_id, 84378, "Has proper account id")
        self.assertEquals(
            course.term.sis_term_id, "2013-spring", "SIS term id")
        self.assertEquals(course.term.term_id, 810, "Term id")
        self.assertEquals(course.public_syllabus, False, "public_syllabus")
        self.assertEquals(
            course.workflow_state, "unpublished", "workflow_state")
        self.assertTrue(course.is_unpublished)

    def test_course_with_params(self):
        canvas = Courses()
        course1 = canvas.get_course(149650, params={"include": ["term"]})

        self.assertEquals(
            course1.term.term_id, 810, "Course contains term data")
        self.assertEquals(
            course1.syllabus_body, None,
            "Course doesn't contain syllabus_body")

        course2 = canvas.get_course(
            149650, params={"include": ["syllabus_body"]})

        self.assertEquals(
            course2.syllabus_body, "Syllabus", "Course contains syllabus_body")
        self.assertEquals(
            course1.term.term_id, 810, "Course contains term data")

    def test_courses(self):
        canvas = Courses()

        courses = canvas.get_courses_in_account_by_sis_id(
            'uwcourse:seattle:arts-&-sciences:amath:amath',
            {'published': True})

        self.assertEquals(len(courses), 7, "Too few courses")

        course = courses[2]

        self.assertEquals(course.course_id, 141414, "Has proper course id")
        self.assertEquals(course.sis_course_id, "2013-spring-AMATH-403-A")
        self.assertEquals(course.sws_course_id(), "2013,spring,AMATH,403/A")
        self.assertEquals(
            course.name,
            "AMATH 403 A: Methods For Partial Differential Equations")
        self.assertEquals(course.account_id, 333333, "Has proper account id")
        self.assertEquals(
            course.course_url, "https://canvas.uw.edu/courses/141414",
            "Has proper course url")

    def test_published_courses(self):
        canvas = Courses()

        courses = canvas.get_published_courses_in_account_by_sis_id(
            'uwcourse:seattle:arts-&-sciences:amath:amath')

        self.assertEquals(len(courses), 7, "Too few courses")

        course = courses[2]

        self.assertEquals(course.course_id, 141414, "Has proper course id")
        self.assertEquals(course.sis_course_id, "2013-spring-AMATH-403-A")
        self.assertEquals(course.sws_course_id(), "2013,spring,AMATH,403/A")
        self.assertEquals(
            course.name,
            "AMATH 403 A: Methods For Partial Differential Equations")
        self.assertEquals(course.account_id, 333333, "Has proper account id")
        self.assertEquals(
            course.course_url, "https://canvas.uw.edu/courses/141414",
            "Has proper course url")

    def test_courses_by_regid(self):
        canvas = Courses()

        courses = canvas.get_courses_for_regid(
            "9136CCB8F66711D5BE060004AC494FFE")

        self.assertEquals(len(courses), 1, "Has 1 canvas enrollment")

        course = courses[0]

        self.assertEquals(
            course.course_url, "https://canvas.uw.edu/courses/149650",
            "Has proper course url")
        self.assertEquals(
            course.sis_course_id, "2013-spring-PHYS-121-A",
            "Course doesnt contain SIS ID")
        self.assertEquals(
            course.sws_course_id(), "2013,spring,PHYS,121/A",
            "Course doesnt contain SIS ID")
        self.assertEquals(course.account_id, 84378, "Has proper account id")

    def test_sis_id(self):
        course = CanvasCourse()
        self.assertEquals(course.sws_course_id(), None)
        self.assertEquals(course.sws_instructor_regid(), None)
        self.assertEquals(course.is_academic_sis_id(), False)

        course = CanvasCourse(sis_course_id="2013-spring-PHYS-121-A")
        self.assertEquals(course.sws_course_id(), "2013,spring,PHYS,121/A")
        self.assertEquals(course.sws_instructor_regid(), None)
        self.assertEquals(course.is_academic_sis_id(), True)

        course = CanvasCourse(
            sis_course_id=(
                "2013-spring-PHYS-599-A-9136CCB8F66711D5BE060004AC494FFE"))
        self.assertEquals(course.sws_course_id(), "2013,spring,PHYS,599/A")
        self.assertEquals(
            course.sws_instructor_regid(), "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEquals(course.is_academic_sis_id(), True)

        course = CanvasCourse(sis_course_id="course_123456")
        self.assertEquals(course.sws_course_id(), None)
        self.assertEquals(course.sws_instructor_regid(), None)
        self.assertEquals(course.is_academic_sis_id(), False)

    @mock.patch.object(Courses, '_post_resource')
    def test_create_course(self, mock_create):
        mock_create.return_value = None
        canvas = Courses()
        canvas.create_course(88888, "Created Course")
        mock_create.assert_called_with(
            '/api/v1/accounts/88888/courses',
            {'course': {'name': 'Created Course'}})

    @mock.patch.object(Courses, '_put_resource')
    def test_update_sis_id(self, mock_update):
        mock_update.return_value = None
        canvas = Courses()
        canvas.update_sis_id(149650, "NEW_SIS_ID")
        mock_update.assert_called_with(
            '/api/v1/courses/149650',
            {'course': {'sis_course_id': 'NEW_SIS_ID'}})
