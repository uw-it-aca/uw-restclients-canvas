from uw_canvas import Canvas
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.models import CanvasCourse

COURSES_API = "/api/v1/courses/{}"


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

        url = COURSES_API.format(course_id)
        return CanvasCourse(data=self._get_resource(url, params=params))

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

        url = ACCOUNTS_API.format(account_id) + "/courses"

        courses = []
        for data in self._get_paged_resource(url, params=params):
            courses.append(CanvasCourse(data=data))
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
        self._as_user = regid
        data = self._get_resource("/api/v1/courses", params=params)
        self._as_user = None

        courses = []
        for datum in data:
            if "sis_course_id" in datum:
                courses.append(CanvasCourse(data=datum))
            else:
                courses.append(self.get_course(datum["id"], params))

        return courses

    def create_course(self, account_id, course_name):
        """
        Create a canvas course with the given subaccount id and course name.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.create
        """
        url = ACCOUNTS_API.format(account_id) + "/courses"
        body = {"course": {"name": course_name}}
        return CanvasCourse(data=self._post_resource(url, body))

    def update_sis_id(self, course_id, sis_course_id):
        """
        Updates the SIS ID for the course identified by the passed course ID.

        https://canvas.instructure.com/doc/api/courses.html#method.courses.update
        """
        url = COURSES_API.format(course_id)
        body = {"course": {"sis_course_id": sis_course_id}}
        return CanvasCourse(data=self._put_resource(url, body))
