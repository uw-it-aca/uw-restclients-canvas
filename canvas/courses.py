from restclients.canvas import Canvas
from restclients.models.canvas import CanvasCourse, CanvasTerm
import re


class Courses(Canvas):
    def get_course(self, course_id, params={}):
        """
        Return course resource for given canvas course id.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.show
        """
        include = params.get("include", [])
        if "term" not in include:
            include.append("term")
        params["include"] = include

        url = "/api/v1/courses/%s" % (course_id)
        return self._course_from_json(self._get_resource(url, params=params))

    def get_course_by_sis_id(self, sis_course_id, params={}):
        """
        Return course resource for given sis id.
        """
        return self.get_course(self._sis_id(sis_course_id, sis_field="course"),
                               params)

    def get_courses_in_account(self, account_id, params={}):
        """
        Returns a list of courses for the passed account ID.

        https://canvas.instructure.com/doc/api/accounts.html#method.accounts.courses_api
        """
        if "published" in params:
            params["published"] = "true" if params["published"] else ""

        url = "/api/v1/accounts/%s/courses" % (account_id)

        courses = []
        for data in self._get_paged_resource(url, params=params):
            courses.append(self._course_from_json(data))
        return courses

    def get_courses_in_account_by_sis_id(self, sis_account_id, params={}):
        """
        Return a list of courses for the passed account SIS ID.
        """
        return self.get_courses_in_account(
            self._sis_id(sis_account_id, sis_field="account"), params)

    def get_published_courses_in_account(self, account_id, params={}):
        """
        Return a list of published courses for the passed account ID.
        """
        params["published"] = True
        return self.get_courses_in_account(account_id, params)

    def get_published_courses_in_account_by_sis_id(self, sis_account_id,
                                                   params={}):
        """
        Return a list of published courses for the passed account SIS ID.
        """

        return self.get_published_courses_in_account(
            self._sis_id(sis_account_id, sis_field="account"), params)

    def get_courses_for_regid(self, regid, params={}):
        """
        Return a list of courses for the passed regid.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.index
        """
        params["as_user_id"] = self._sis_id(regid, sis_field="user")

        data = self._get_resource("/api/v1/courses", params=params)
        del params["as_user_id"]

        courses = []
        for datum in data:
            if "sis_course_id" in datum:
                courses.append(self._course_from_json(datum))
            else:
                courses.append(self.get_course(datum["id"], params))

        return courses

    def create_course(self, account_id, course_name):
        """
        Create a canvas course with the given subaccount id and course name.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.create
        """
        url = "/api/v1/accounts/%s/courses" % account_id
        body = {"course": {"name": course_name}}

        data = self._post_resource(url, body)

        return self._course_from_json(data)

    def update_sis_id(self, course_id, sis_course_id):
        """
        Updates the SIS ID for the course identified by the passed course ID.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.update
        """
        url = "/api/v1/courses/%s" % course_id
        body = {"course": {"sis_course_id": sis_course_id}}

        data = self._put_resource(url, body)

        return self._course_from_json(data)

    def _course_from_json(self, data):
        course = CanvasCourse()
        course.course_id = data["id"]
        course.sis_course_id = data.get("sis_course_id", None)
        course.account_id = data["account_id"]
        course.code = data["course_code"]
        course.name = data["name"]
        course.workflow_state = data["workflow_state"]
        course.public_syllabus = data["public_syllabus"]

        course_url = data["calendar"]["ics"]
        course_url = re.sub(r"(.*?[a-z]/).*", r"\1", course_url)
        course.course_url = "%scourses/%s" % (course_url, data["id"])

        # Optional attributes specified in the course URL
        if "term" in data:
            canvas_term = data["term"]
            course.term = CanvasTerm(
                term_id=canvas_term.get("id"),
                sis_term_id=canvas_term.get("sis_term_id", None),
                name=canvas_term.get("name"))

        if "syllabus_body" in data:
            course.syllabus_body = data["syllabus_body"]

        return course
