from uw_canvas import Canvas
from uw_canvas.courses import Courses
from uw_canvas.models import CanvasEnrollment
import dateutil.parser
import re


class Enrollments(Canvas):
    def get_enrollments_for_course(self, course_id, params={}):
        """
        Return a list of all enrollments for the passed course_id.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.index
        """
        url = "/api/v1/courses/%s/enrollments" % (course_id)

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollment = self._enrollment_from_json(datum)
            enrollments.append(enrollment)

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
        url = "/api/v1/sections/%s/enrollments" % (section_id)

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            enrollment = self._enrollment_from_json(datum)
            enrollments.append(enrollment)

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
        url = "/api/v1/users/%s/enrollments" % (
            self._sis_id(regid, sis_field="user"))

        courses = Courses() if include_courses else None

        enrollments = []
        for datum in self._get_paged_resource(url, params=params):
            if include_courses:
                course_id = datum["course_id"]
                course = courses.get_course(course_id)

                if course.sis_course_id is not None:
                    enrollment = self._enrollment_from_json(datum)
                    enrollment.course = course
                    # the following 3 lines are not removed
                    # to be backward compatible.
                    enrollment.course_url = course.course_url
                    enrollment.course_name = course.name
                    enrollment.sis_course_id = course.sis_course_id
                    enrollments.append(enrollment)
            else:
                enrollment = self._enrollment_from_json(datum)
                enrollment.course_url = re.sub(
                    r'/users/\d+$', '', enrollment.html_url)
                enrollments.append(enrollment)

        return enrollments

    def enroll_user(self, course_id, user_id, enrollment_type, params=None):
        """
        Enroll a user into a course.

        https://canvas.instructure.com/doc/api/enrollments.html#method.enrollments_api.create
        """
        url = "/api/v1/courses/%s/enrollments" % course_id

        if not params:
            params = {}

        params["user_id"] = user_id
        params["type"] = enrollment_type

        data = self._post_resource(url, {"enrollment": params})
        return self._enrollment_from_json(data)

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

    def _enrollment_from_json(self, data):
        enrollment = CanvasEnrollment()
        enrollment.user_id = data["user_id"]
        enrollment.course_id = data["course_id"]
        enrollment.section_id = data["course_section_id"]
        enrollment.role = data["type"]
        enrollment.status = data["enrollment_state"]
        enrollment.html_url = data["html_url"]
        enrollment.total_activity_time = data["total_activity_time"]
        enrollment.limit_privileges_to_course_section = data.get(
            "limit_privileges_to_course_section", False)
        if data["last_activity_at"] is not None:
            date_str = data["last_activity_at"]
            enrollment.last_activity_at = dateutil.parser.parse(date_str)

        enrollment.sis_course_id = data.get("sis_course_id", None)
        enrollment.sis_section_id = data.get("sis_section_id", None)

        if "user" in data:
            user_data = data["user"]
            enrollment.name = user_data.get("name", None)
            enrollment.sortable_name = user_data.get("sortable_name", None)
            enrollment.login_id = user_data.get("login_id", None)
            enrollment.sis_user_id = user_data.get("sis_user_id", None)

        if "grades" in data:
            grade_data = data["grades"]
            enrollment.current_score = grade_data.get("current_score", None)
            enrollment.final_score = grade_data.get("final_score", None)
            enrollment.current_grade = grade_data.get("current_grade", None)
            enrollment.final_grade = grade_data.get("final_grade", None)
            enrollment.grade_html_url = grade_data.get("html_url", None)
        return enrollment
