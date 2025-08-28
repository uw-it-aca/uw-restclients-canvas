# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.accounts import ACCOUNTS_API
from restclients_core.exceptions import DataFailureException


class LTIRegistrations(Canvas):
    """
    Implementation of the Canvas LTI Registration API:
        https://developerdocs.instructure.com
            /services/canvas/resources/lti_registrations
    """
    @property
    def base_url(self):
        return ACCOUNTS_API.format(self._canvas_account_id)

    def registration_url(self, registration_id=None):
        """
        Return the LTI Registrations URL
        """
        url = f"{self.base_url}/lti_registrations"
        return f"{url}/{registration_id}" if registration_id else url

    def get_registrations(self, params={}):
        """
        Return all LTI registrations
        """
        payload_key = 'data'
        url = self.registration_url()
        return self._get_paged_resource(
            url, params, payload_key).get(payload_key, [])

    def get_registration_by_id(self, registration_id, params={}):
        """
        Return LTI Registrations URL for a specific client id
        """
        url = self.registration_url(registration_id)
        return self._get_resource(url, params=params)

    def update_registration(self, registration_id, json_data):
        """
        Update the LTI registration identified by registration_id
        with the given json data.
        """
        return self._put_resource(
            self.registration_url(registration_id), body=json_data)
