# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.enrollments import Enrollments
from uw_canvas.models import CanvasEnrollment
import mock


@fdao_canvas_override
class CanvasTestEnrollment(TestCase):
    def test_enrollments_for_course_id(self):
        canvas = Enrollments()

        enrollments = canvas.get_enrollments_for_course_by_sis_id(
            "2013-autumn-PHYS-248-A")

        self.assertEqual(len(enrollments), 2, "Has 2 canvas enrollments")

        students = canvas.get_enrollments_for_course_by_sis_id(
            "2013-autumn-PHYS-248-A", {"role": "student"})

        self.assertEqual(len(students), 1, "Has 1 student enrollments")

    def test_enrollments_for_section_id(self):
        canvas = Enrollments()

        enrollments = canvas.get_enrollments_for_section_by_sis_id(
            "2013-autumn-PHYS-248-A--")
        self.assertEqual(len(enrollments), 2, "Has 2 canvas enrollments")

        students = canvas.get_enrollments_for_section_by_sis_id(
            "2013-autumn-PHYS-248-A--", {"role": "student"})

        self.assertEqual(len(students), 1, "Has 1 student enrollments")

        enr = students[0]
        self.assertEqual(enr.current_score, 77.76)
        self.assertEqual(enr.current_grade, None)
        self.assertEqual(enr.final_score, 53.37)
        self.assertEqual(enr.final_grade, None)
        self.assertEqual(enr.unposted_current_score, 58.32)
        self.assertEqual(enr.unposted_final_score, 55.37)
        self.assertEqual(enr.unposted_current_grade, None)
        self.assertEqual(enr.unposted_final_grade, None)
        self.assertEqual(enr.override_score, 80.0)
        self.assertEqual(enr.override_grade, None)

        self.assertEquals(enr.sis_course_id, "2013-autumn-PHYS-248-A")
        self.assertEquals(enr.sws_course_id(), "2013,autumn,PHYS,248/A")
        self.assertEquals(enr.sis_section_id, "2013-autumn-PHYS-248-A--")
        self.assertEquals(enr.sws_section_id(), "2013,autumn,PHYS,248/A")

    # Expected values will have to change when the json files are updated
    def test_enrollments_by_regid(self):
        canvas = Enrollments()

        enrollments = canvas.get_enrollments_for_regid(
            "9136CCB8F66711D5BE060004AC494FFE", include_courses=True)

        self.assertEquals(len(enrollments), 2, "Has 2 canvas enrollments")

        enrollment = enrollments[0]
        self.assertEquals(enrollment.course_url,
                          "https://test.canvas.edu/courses/149650")
        self.assertEquals(enrollment.sis_course_id, "2013-spring-PHYS-121-A")
        self.assertEquals(enrollment.sws_course_id(), "2013,spring,PHYS,121/A")
        self.assertEquals(enrollment.sis_user_id,
                          "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEquals(enrollment.course_name, "MECHANICS")
        self.assertIsNotNone(enrollment.course)

        stu_enrollment = enrollments[1]
        self.assertEquals(
            stu_enrollment.grade_html_url,
            "https://test.instructure.com/courses/862539/grades/12345")
        self.assertEquals(stu_enrollment.current_score, 23.0, "Current score")
        self.assertEquals(stu_enrollment.login_id, "javerage", "Login ID")
        self.assertEquals(
            stu_enrollment.sis_user_id, "9136CCB8F66711D5BE060004AC494FFE",
            "SIS User ID")
        self.assertEquals(stu_enrollment.name, "JAMES AVERAGE STUDENT", "Name")
        self.assertEquals(
            enrollment.sortable_name, "STUDENT, JAMES AVERAGE",
            "Sortable Name")
        self.assertEquals(
            str(stu_enrollment.last_activity_at), "2012-08-18 23:08:51-06:00",
            "Last activity datetime")
        self.assertEquals(
            stu_enrollment.total_activity_time, 100, "Total activity time")
        self.assertEquals(
            stu_enrollment.status, CanvasEnrollment.STATUS_ACTIVE, "Status")

    def test_pending_enrollments(self):
        canvas = Enrollments()

        enrollments = canvas.get_enrollments_for_course("862539")

        self.assertEquals(len(enrollments), 1, "Has 1 canvas enrollment")

        enrollment = enrollments[0]
        self.assertEquals(enrollment.name, "James Average", "Name")
        self.assertEquals(
            enrollment.sortable_name, "Average, James", "Sortable Name")
        self.assertEquals(enrollment.login_id, None)
        self.assertEquals(
            enrollment.status, CanvasEnrollment.STATUS_INVITED, "Status")

    @mock.patch.object(Enrollments, '_post_resource')
    def test_enroll_user(self, mock_create):
        mock_create.return_value = None
        canvas = Enrollments()

        canvas.enroll_user("862539", "12345", "Student")
        mock_create.assert_called_with(
            '/api/v1/courses/862539/enrollments', {
                'enrollment': {'user_id': '12345', 'type': 'Student'}})

    @mock.patch.object(Enrollments, '_post_resource')
    def test_enroll_user_in_course(self, mock_create):
        mock_create.return_value = None
        canvas = Enrollments()

        canvas.enroll_user_in_course("862539", "12345", "Student",
                                     course_section_id="99999",
                                     role_id="1111", status="active")
        mock_create.assert_called_with(
            '/api/v1/courses/862539/enrollments', {
                'enrollment': {'user_id': '12345', 'type': 'Student',
                               'enrollment_state': 'active',
                               'course_section_id': '99999',
                               'role_id': '1111'}})

    def test_sis_import_roles(self):
        self.assertEqual(CanvasEnrollment.sis_import_role('StudentEnrollment'),
                         'student')
        self.assertEqual(CanvasEnrollment.sis_import_role('Student'),
                         'student')
        self.assertEqual(CanvasEnrollment.sis_import_role('student'),
                         'student')
        self.assertEqual(CanvasEnrollment.sis_import_role('TaEnrollment'),
                         'ta')
        self.assertEqual(CanvasEnrollment.sis_import_role('TA'), 'ta')
        self.assertEqual(CanvasEnrollment.sis_import_role('Librarian'),
                         'Librarian')
        self.assertEqual(CanvasEnrollment.sis_import_role('Unknown Role'),
                         None)
