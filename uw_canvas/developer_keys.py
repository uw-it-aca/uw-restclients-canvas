# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.accounts import ACCOUNTS_API
from restclients_core.exceptions import DataFailureException


DEVELOPER_KEY_API = "/api/lti/developer_keys/{}/tool_configuration"


class DeveloperKeys(Canvas):
    def get_developer_keys(self, params={}):
        """
        Return developer key data for the canvas account.

        At time of writing, this is an undocumented API endpoint, but
        was referenced in the Canvas User Community discussion:
        https://community.canvaslms.com/t5/Canvas-Developers-Group/
          API-functions-to-manage-Developer-Keys/m-p/544282
        """
        url = ACCOUNTS_API.format(self._canvas_account_id) + "/developer_keys"

        try:
            developer_keys = []
            for keys in self._get_paged_resource(url, params=params):
                developer_keys.append(keys)

            return developer_keys
        except DataFailureException as err:
            if err.status == 404:
                # log that api may be no longer supported?
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
