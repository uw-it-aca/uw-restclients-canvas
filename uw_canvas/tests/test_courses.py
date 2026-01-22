# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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

        self.assertEqual(course.course_id, 149650, "Has proper course id")
        self.assertEqual(
            course.course_url, "https://canvas.uw.edu/courses/149650",
            "Has proper course url")
        self.assertEqual(course.sis_course_id, "2013-spring-PHYS-121-A")
        self.assertEqual(course.sws_course_id(), "2013,spring,PHYS,121/A")
        self.assertEqual(course.sws_instructor_regid(), None)
        self.assertEqual(course.is_academic_sis_id(), True)
        self.assertEqual(course.account_id, 84378, "Has proper account id")
        self.assertEqual(
            course.term.sis_term_id, "2013-spring", "SIS term id")
        self.assertEqual(course.term.term_id, 810, "Term id")
        self.assertEqual(course.is_public, False, "is_public")
        self.assertEqual(
            course.is_public_to_auth_users, False, "is_public_to_auth_users")
        self.assertEqual(course.public_syllabus, False, "public_syllabus")
        self.assertEqual(
            course.workflow_state, "unpublished", "workflow_state")
        self.assertEqual(
            course.grading_standard_id, 25, "grading_standard_id")
        self.assertTrue(course.is_unpublished)
        self.assertEqual(
            str(course.created_at), '2013-05-01 00:00:00-06:00')

    def test_course_with_params(self):
        canvas = Courses()
        course1 = canvas.get_course(149650, params={"include": ["term"]})

        self.assertEqual(
            course1.term.term_id, 810, "Course contains term data")
        self.assertEqual(
            course1.syllabus_body, None,
            "Course doesn't contain syllabus_body")

        course2 = canvas.get_course(
            149650, params={"include": ["syllabus_body"]})

        self.assertEqual(
            course2.syllabus_body, "Syllabus", "Course contains syllabus_body")
        self.assertEqual(
            course1.term.term_id, 810, "Course contains term data")

    def test_courses(self):
        canvas = Courses()

        courses = canvas.get_courses_in_account_by_sis_id(
            'uwcourse:seattle:arts-&-sciences:amath:amath',
            {'published': True})

        self.assertEqual(len(courses), 7, "Too few courses")

        course = courses[2]

        self.assertEqual(course.course_id, 141414, "Has proper course id")
        self.assertEqual(course.sis_course_id, "2013-spring-AMATH-403-A")
        self.assertEqual(course.sws_course_id(), "2013,spring,AMATH,403/A")
        self.assertEqual(
            course.name,
            "AMATH 403 A: Methods For Partial Differential Equations")
        self.assertEqual(course.account_id, 333333, "Has proper account id")
        self.assertEqual(
            course.course_url, "https://canvas.uw.edu/courses/141414",
            "Has proper course url")

    def test_published_courses(self):
        canvas = Courses()

        courses = canvas.get_published_courses_in_account_by_sis_id(
            'uwcourse:seattle:arts-&-sciences:amath:amath')

        self.assertEqual(len(courses), 7, "Too few courses")

        course = courses[2]

        self.assertEqual(course.course_id, 141414, "Has proper course id")
        self.assertEqual(course.sis_course_id, "2013-spring-AMATH-403-A")
        self.assertEqual(course.sws_course_id(), "2013,spring,AMATH,403/A")
        self.assertEqual(
            course.name,
            "AMATH 403 A: Methods For Partial Differential Equations")
        self.assertEqual(course.account_id, 333333, "Has proper account id")
        self.assertEqual(
            course.course_url, "https://canvas.uw.edu/courses/141414",
            "Has proper course url")

    def test_courses_by_regid(self):
        canvas = Courses()

        courses = canvas.get_courses_for_regid(
            "9136CCB8F66711D5BE060004AC494FFE")

        self.assertEqual(len(courses), 1, "Has 1 canvas enrollment")

        course = courses[0]

        self.assertEqual(
            course.course_url, "https://canvas.uw.edu/courses/149650",
            "Has proper course url")
        self.assertEqual(
            course.sis_course_id, "2013-spring-PHYS-121-A",
            "Course doesnt contain SIS ID")
        self.assertEqual(
            course.sws_course_id(), "2013,spring,PHYS,121/A",
            "Course doesnt contain SIS ID")
        self.assertEqual(course.account_id, 84378, "Has proper account id")

    def test_sis_id(self):
        course = CanvasCourse()
        self.assertEqual(course.sws_course_id(), None)
        self.assertEqual(course.sws_instructor_regid(), None)
        self.assertEqual(course.is_academic_sis_id(), False)

        course = CanvasCourse(sis_course_id="2013-spring-PHYS-121-A")
        self.assertEqual(course.sws_course_id(), "2013,spring,PHYS,121/A")
        self.assertEqual(course.sws_instructor_regid(), None)
        self.assertEqual(course.is_academic_sis_id(), True)

        course = CanvasCourse(sis_course_id="2013-autumn-GEN ST-199-A7")
        self.assertEqual(course.sws_course_id(), "2013,autumn,GEN ST,199/A7")
        self.assertEqual(course.sws_instructor_regid(), None)
        self.assertEqual(course.is_academic_sis_id(), True)

        course = CanvasCourse(
            sis_course_id=(
                "2013-spring-PHYS-599-A-9136CCB8F66711D5BE060004AC494FFE"))
        self.assertEqual(course.sws_course_id(), "2013,spring,PHYS,599/A")
        self.assertEqual(
            course.sws_instructor_regid(), "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEqual(course.is_academic_sis_id(), True)

        course = CanvasCourse(sis_course_id="course_123456")
        self.assertEqual(course.sws_course_id(), None)
        self.assertEqual(course.sws_instructor_regid(), None)
        self.assertEqual(course.is_academic_sis_id(), False)

    @mock.patch.object(Courses, '_post_resource')
    def test_create_course(self, mock_create):
        mock_create.return_value = None
        canvas = Courses()
        canvas.create_course(88888, "Created Course")
        mock_create.assert_called_with(
            '/api/v1/accounts/88888/courses',
            {'course': {'name': 'Created Course'}})

        canvas.create_course(88888, "Created Course", term_id="12345")
        mock_create.assert_called_with(
            '/api/v1/accounts/88888/courses',
            {'course': {'name': 'Created Course', 'term_id': '12345'}})

    @mock.patch.object(Courses, '_put_resource')
    def test_update_sis_id(self, mock_update):
        mock_update.return_value = None
        canvas = Courses()
        canvas.update_sis_id(149650, "NEW_SIS_ID")
        mock_update.assert_called_with(
            '/api/v1/courses/149650',
            {'course': {'sis_course_id': 'NEW_SIS_ID'}})

    @mock.patch.object(Courses, '_put_resource')
    def test_update_visibility(self, mock_update):
        mock_update.return_value = None
        canvas = Courses()
        canvas.update_visibility(149650, False, False)
        mock_update.assert_called_with(
            '/api/v1/courses/149650',
            {'course': {'is_public': False, 'is_public_to_auth_users': False}})

    @mock.patch.object(Courses, '_delete_resource')
    def test_delete_course(self, mock_delete):
        mock_delete.return_value = None
        canvas = Courses()

        canvas.delete_course(149650)
        mock_delete.assert_called_with(
            '/api/v1/courses/149650', params={'event': 'delete'})

        canvas.delete_course(149650, event='conclude')
        mock_delete.assert_called_with(
            '/api/v1/courses/149650', params={'event': 'conclude'})

    @mock.patch.object(Courses, '_put_resource')
    def test_publish_course(self, mock_put):
        mock_put.return_value = {
            'id': 149650,
            'account_id': 84378,
            'course_code': 'PHYS 121',
            'name': 'MECHANICS',
            'workflow_state': 'available',
            'is_public': False,
            'is_public_to_auth_users': False,
            'public_syllabus': False,
            'calendar': {
                'ics':
                    'https://canvas.uw.edu/feeds/calendars/course_test.ics'
                }
        }
        canvas = Courses()
        canvas.publish_course(149650)
        mock_put.assert_called_with(
            '/api/v1/courses/149650',
            {'course': {'event': 'offer'}})

    @mock.patch.object(Courses, 'get_course_by_sis_id')
    @mock.patch.object(Courses, 'publish_course')
    def test_publish_course_by_sis_id(self, mock_publish, mock_get_course):
        # Test successful publish
        mock_course = CanvasCourse(data={
            'id': 149650,
            'account_id': 84378,
            'course_code': 'PHYS 121',
            'name': 'MECHANICS',
            'workflow_state': 'unpublished',
            'is_public': False,
            'is_public_to_auth_users': False,
            'public_syllabus': False,
            'calendar': {
                'ics':
                    'https://canvas.uw.edu/feeds/calendars/course_test.ics'
                }
        })
        mock_get_course.return_value = mock_course
        mock_publish.return_value = CanvasCourse(data={
            'id': 149650,
            'account_id': 84378,
            'course_code': 'PHYS 121',
            'name': 'MECHANICS',
            'workflow_state': 'available',
            'is_public': False,
            'is_public_to_auth_users': False,
            'public_syllabus': False,
            'calendar': {
                'ics':
                    'https://canvas.uw.edu/feeds/calendars/course_test.ics'
                }
        })

        canvas = Courses()
        result = canvas.publish_course_by_sis_id('2013-spring-PHYS-121-A')

        mock_get_course.assert_called_with('2013-spring-PHYS-121-A')
        mock_publish.assert_called_with(149650)
        self.assertEqual(result.workflow_state, 'available')

        # Test course not found
        mock_get_course.return_value = None
        result = canvas.publish_course_by_sis_id('nonexistent-course')
        self.assertIsNone(result)

    @mock.patch.object(Courses, '_put_resource')
    def test_unpublish_course(self, mock_put):
        mock_put.return_value = {
            'id': 149650,
            'account_id': 84378,
            'course_code': 'PHYS 121',
            'name': 'MECHANICS',
            'workflow_state': 'unpublished',
            'is_public': False,
            'is_public_to_auth_users': False,
            'public_syllabus': False,
            'calendar': {
                'ics':
                    'https://canvas.uw.edu/feeds/calendars/course_test.ics'
                }
        }
        canvas = Courses()
        canvas.unpublish_course(149650)
        mock_put.assert_called_with(
            '/api/v1/courses/149650',
            {'course': {'event': 'claim'}})

    @mock.patch.object(Courses, 'get_course_by_sis_id')
    @mock.patch.object(Courses, 'unpublish_course')
    def test_unpublish_course_by_sis_id(self, mock_unpublish, mock_get_course):
        # Test successful unpublish
        mock_course = CanvasCourse(data={
            'id': 149650,
            'account_id': 84378,
            'course_code': 'PHYS 121',
            'name': 'MECHANICS',
            'workflow_state': 'available',
            'is_public': False,
            'is_public_to_auth_users': False,
            'public_syllabus': False,
            'calendar': {
                'ics':
                    'https://canvas.uw.edu/feeds/calendars/course_test.ics'
                }
        })
        mock_get_course.return_value = mock_course
        mock_unpublish.return_value = CanvasCourse(data={
            'id': 149650,
            'account_id': 84378,
            'course_code': 'PHYS 121',
            'name': 'MECHANICS',
            'workflow_state': 'unpublished',
            'is_public': False,
            'is_public_to_auth_users': False,
            'public_syllabus': False,
            'calendar': {
                'ics':
                    'https://canvas.uw.edu/feeds/calendars/course_test.ics'
                }
        })

        canvas = Courses()
        result = canvas.unpublish_course_by_sis_id('2013-spring-PHYS-121-A')

        mock_get_course.assert_called_with('2013-spring-PHYS-121-A')
        mock_unpublish.assert_called_with(149650)
        self.assertEqual(result.workflow_state, 'unpublished')

        # Test course not found
        mock_get_course.return_value = None
        result = canvas.unpublish_course_by_sis_id('nonexistent-course')
        self.assertIsNone(result)
