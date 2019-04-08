from uw_canvas import Canvas
from uw_canvas.courses import Courses, COURSES_API
from uw_canvas.sections import SECTIONS_API
from uw_canvas.users import USERS_API
from uw_canvas.models import CanvasEnrollment
import re


class Enrollments(Canvas):
    def get_enrollments_for_course(self, course_id, params={}):
        """
        Return a list of all enrollments for the passed course_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = COURSES_API.format(course_id) + "/enrollments"

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollments.append(CanvasEnrollment(data=datum))

        return enrollments

    def get_enrollments_for_course_by_sis_id(self, sis_course_id, params={}):
        """
        Return a list of all enrollments for the passed course sis id.
        """
        return self.get_enrollments_for_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def get_enrollments_for_section(self, section_id, params={}):
        """
        Return a list of all enrollments for the passed section_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = SECTIONS_API.format(section_id) + "/enrollments"

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollments.append(CanvasEnrollment(data=datum))

        return enrollments

    def get_enrollments_for_section_by_sis_id(self, sis_section_id, params={}):
        """
        Return a list of all enrollments for the passed section sis id.
        """
        return self.get_enrollments_for_section(
            self._sis_id(sis_section_id, sis_field="section"), params)

    def get_enrollments_for_regid(self, regid, params={},
                                  include_courses=True):
        """
        Return a list of enrollments for the passed user regid.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        sis_user_id = self._sis_id(regid, sis_field="user")
        url = USERS_API.format(sis_user_id) + "/enrollments"

        courses = Courses() if include_courses else None

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollment = CanvasEnrollment(data=datum)
            if include_courses:
                course_id = datum["course_id"]
                course = courses.get_course(course_id)

                if course.sis_course_id is not None:
                    enrollment.course = course
                    # the following 3 lines are not removed
                    # to be backward compatible.
                    enrollment.course_url = course.course_url
                    enrollment.course_name = course.name
                    enrollment.sis_course_id = course.sis_course_id
            else:
                enrollment.course_url = re.sub(
                    r'/users/\d+$', '', enrollment.html_url)

            enrollments.append(enrollment)
        return enrollments

    def enroll_user(self, course_id, user_id, enrollment_type, params=None):
        """
        Enroll a user into a course.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create
        """
        url = COURSES_API.format(course_id) + "/enrollments"

        if not params:
            params = {}

        params["user_id"] = user_id
        params["type"] = enrollment_type

        data = self._post_resource(url, {"enrollment": params})
        return CanvasEnrollment(data=data)

    def enroll_user_in_course(self, course_id, user_id, enrollment_type,
                              course_section_id=None, role_id=None,
                              status="active"):
        params = {
            "user_id": user_id,
            "type": enrollment_type,
            "enrollment_state": status
        }

        if course_section_id:
            params['course_section_id'] = course_section_id

        if role_id:
            params['role_id'] = role_id

        return self.enroll_user(course_id, user_id, enrollment_type, params)
