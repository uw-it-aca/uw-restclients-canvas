# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


"""
This is the interface for interacting with Instructure's Canvas web services.
"""

from commonconf import settings
from urllib.parse import quote
import warnings
import json
import re
from restclients_core.exceptions import DataFailureException
from uw_canvas.dao import Canvas_DAO

DEFAULT_PAGINATION = 0
MASQUERADING_USER = None


def deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=2)


class MissingAccountID(Exception):
    def __str__(self):
        return "This API requires CANVAS_ACCOUNT_ID in settings."


class Canvas(object):
    """
    The Canvas object has methods for getting information
    about accounts, courses, enrollments and users within
    Canvas
    """

    def __init__(self,
                 per_page=DEFAULT_PAGINATION,
                 as_user=MASQUERADING_USER,
                 canvas_api_host=None):
        """
        Prepares for paginated responses
        """
        self._per_page = per_page
        self._as_user = as_user
        self._re_canvas_id = re.compile(r'^\d{2,12}$')
        self._canvas_account_id = getattr(
            settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID', None)
        self._DAO = Canvas_DAO(canvas_api_host=canvas_api_host)

    def get_courses_for_regid(self, regid):
        deprecation("Use uw_canvas.courses.get_courses_for_regid")
        from uw_canvas.courses import Courses
        return Courses().get_courses_for_regid(regid)

    def get_enrollments_for_regid(self, regid):
        deprecation(
            "Use uw_canvas.enrollments.get_enrollments_for_regid")
        from uw_canvas.enrollments import Enrollments
        return Enrollments().get_enrollments_for_regid(regid)

    def get_term_by_sis_id(self, sis_term_id):
        deprecation("Use uw_canvas.terms.get_term_by_sis_id")
        from uw_canvas.terms import Terms
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
        return quote('sis_{}_id:{}'.format(sis_field, sis_id))

    def _params(self, params):
        if params and len(params):
            p = []
            for key in sorted(params.keys()):
                val = params[key]
                if isinstance(val, list):
                    p.extend([key + '[]=' + quote(str(v)) for v in val])
                else:
                    p.append(key + '=' + quote(str(val)))

            return "?" + '&'.join(p)
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
            except Exception:
                return

    def _get_resource_url(self, url, auto_page, data_key):
        """
        Canvas GET method on a full url. Return representation of the
        requested resource, chasing pagination links to coalesce resources
        if indicated.
        """
        headers = {'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        response = self._DAO.getURL(url, headers)

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
        if ('as_user_id' not in params and self._as_user is not None):
            if self.valid_canvas_id(self._as_user):
                as_user = self._as_user
            else:
                as_user = 'sis_user_id:{}'.format(self._as_user)
            params['as_user_id'] = as_user

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

        full_url = url + self._params(params)
        return self._get_resource_url(full_url, auto_page, data_key)

    def _get_resource(self, url, params=None, data_key=None):
        """
        Canvas GET method. Return representation of the requested resource.
        """
        if not params:
            params = {}

        self._set_as_user(params)

        full_url = url + self._params(params)

        return self._get_resource_url(full_url, True, data_key)

    def _put_resource(self, url, body={}):
        """
        Canvas PUT method.
        """
        params = {}
        self._set_as_user(params)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        url = url + self._params(params)
        response = self._DAO.putURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 201 or
                response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _post_resource(self, url, body):
        """
        Canvas POST method.
        """
        params = {}
        self._set_as_user(params)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        url = url + self._params(params)
        response = self._DAO.postURL(url, headers, json.dumps(body))

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

    def _delete_resource(self, url, params={}):
        """
        Canvas DELETE method.
        """
        self._set_as_user(params)
        headers = {'Accept': 'application/json',
                   'Connection': 'keep-alive'}
        url = url + self._params(params)
        response = self._DAO.deleteURL(url, headers)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return response
