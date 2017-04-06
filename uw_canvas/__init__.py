"""
This is the interface for interacting with Instructure's Canvas web services.
"""
from restclients_core.exceptions import DataFailureException
from uw_canvas.dao import Canvas_DAO
try:
    from urllib.parse import quote, unquote
except ImportError:
    from urllib import quote, unquote
import warnings
import json
import re


DEFAULT_PAGINATION = 0
MASQUERADING_USER = None


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


class Canvas(object):
    """
    The Canvas object has methods for getting information
    about accounts, courses, enrollments and users within
    Canvas
    """

    def __init__(self, per_page=DEFAULT_PAGINATION, as_user=MASQUERADING_USER):
        """
        Prepares for paginated responses
        """
        self._per_page = per_page
        self._re_canvas_id = re.compile(r'^\d{2,12}$')

        if as_user:
            self._as_user = as_user if (
                self.valid_canvas_id(as_user)) else self.sis_user_id(as_user)

    def get_courses_for_regid(self, regid):
        deprecation("Use restclients.canvas.courses.get_courses_for_regid")
        from restclients.canvas.courses import Courses
        return Courses().get_courses_for_regid(regid)

    def get_enrollments_for_regid(self, regid):
        deprecation(
            "Use restclients.canvas.enrollments.get_enrollments_for_regid")
        from restclients.canvas.enrollments import Enrollments
        return Enrollments().get_enrollments_for_regid(regid)

    def get_term_by_sis_id(self, sis_term_id):
        deprecation("Use restclients.canvas.terms.get_term_by_sis_id")
        from restclients.canvas.terms import Terms
        return Terms().get_term_by_sis_id(sis_term_id)

    def valid_canvas_id(self, canvas_id):
        return self._re_canvas_id.match(str(canvas_id)) is not None

    def sis_account_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="account")

    def sis_course_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="course")

    def sis_section_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="section")

    def sis_user_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="user")

    def sis_login_id(self, sis_id):
        return self._sis_id(sis_id, sis_field="login")

    def _sis_id(self, sis_id, sis_field='account'):
        """
        generate sis_id object reference
        """
        return quote('sis_%s_id:%s' % (sis_field, sis_id))

    def _params(self, params):
        if params and len(params):
            p = []
            for key in sorted(params.keys()):
                val = params[key]
                if isinstance(val, list):
                    p.extend([key + '[]=' + str(v) for v in val])
                else:
                    p.append(key + '=' + str(val))

            return "?%s" % ('&'.join(p))
        return ""

    def _next_page(self, response):
        """
        return url path to next page of paginated data
        """
        for link in response.getheader("link", "").split(","):
            try:
                (url, rel) = link.split(";")
                if "next" in rel:
                    return url.lstrip("<").rstrip(">")
            except:
                return

    def _get_resource_url(self, url, auto_page, data_key):
        """
        Canvas GET method on a full url. Return representation of the
        requested resource, chasing pagination links to coalesce resources
        if indicated.
        """
        headers = {'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        response = Canvas_DAO().getURL(url, headers)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        data = json.loads(response.data)

        self.next_page_url = self._next_page(response)
        if auto_page and self.next_page_url:
            if isinstance(data, list):
                data.extend(self._get_resource_url(self.next_page_url, True,
                                                   data_key))
            elif isinstance(data, dict) and data_key is not None:
                data[data_key].extend(self._get_resource_url(
                    self.next_page_url, True, data_key)[data_key])

        return data

    def _set_as_user(self, params):
        if 'as_user_id' not in params and hasattr(self, '_as_user'):
            params['as_user_id'] = self._as_user

    def _get_paged_resource(self, url, params=None, data_key=None):
        """
        Canvas GET method. Return representation of the requested paged
        resource, either the requested page, or chase pagination links to
        coalesce resources.
        """
        if not params:
            params = {}

        self._set_as_user(params)

        auto_page = not ('page' in params or 'per_page' in params)

        if 'per_page' not in params and self._per_page != DEFAULT_PAGINATION:
            params["per_page"] = self._per_page

        full_url = '%s%s' % (url, self._params(params))
        return self._get_resource_url(full_url, auto_page, data_key)

    def _get_resource(self, url, params=None, data_key=None):
        """
        Canvas GET method. Return representation of the requested resource.
        """
        if not params:
            params = {}

        self._set_as_user(params)

        full_url = '%s%s' % (url, self._params(params))

        return self._get_resource_url(full_url, True, data_key)

    def _put_resource(self, url, body):
        """
        Canvas PUT method.
        """
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        response = Canvas_DAO().putURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _post_resource(self, url, body):
        """
        Canvas POST method.
        """
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        response = Canvas_DAO().postURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _delete_resource(self, url):
        """
        Canvas DELETE method.
        """
        headers = {'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        response = Canvas_DAO().deleteURL(url, headers)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return response
