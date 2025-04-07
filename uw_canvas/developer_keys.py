# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.accounts import ACCOUNTS_API
from restclients_core.exceptions import DataFailureException


DEVELOPER_KEY_API = "/api/v1/developer_keys/{}"


class DeveloperKeys(Canvas):
    def get_developer_keys(self, params={}):
        """
        Return developer key data for the canvas account.
        Note: the endpoint to list keys is different from the endpoint for
        PUT/POST/DELETE operations. Both are documented in the Canvas API docs:
        https://canvas.instructure.com/doc/api/developer_keys.html
        """
        url = ACCOUNTS_API.format(self._canvas_account_id) + "/developer_keys"

        try:
            developer_keys = []
            for keys in self._get_paged_resource(url, params=params):
                developer_keys.append(keys)

            return developer_keys
        except DataFailureException as err:
            if err.status == 404:
                return []

            raise

    def get_developer_key_by_id(self, developer_key_id):
        """
        Return developer key data for given key id.
        """
        keys = self.get_developer_keys({'id': developer_key_id})

        return keys[0] if keys else None

    def update_developer_key(self, developer_key_id, json_data):
        """
        Update the developer key identified by developer_key_id with the
        given json data.
        """
        url = DEVELOPER_KEY_API.format(developer_key_id)
        return self._put_resource(url, body=json_data)
