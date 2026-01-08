# Copyright 2026 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas, MissingAccountID
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.models import SISImport as SISImportModel
from uw_canvas.models import SISImportError as SISImportErrorModel
from uw_canvas.dao import Canvas_DAO
from restclients_core.exceptions import DataFailureException
import zipfile
import json
import os


# List of csv files determines sequence of import
CSV_FILES = ["accounts.csv", "users.csv", "terms.csv", "courses.csv",
             "sections.csv", "enrollments.csv", "xlists.csv", "admins.csv"]
SIS_IMPORTS_API = ACCOUNTS_API + "/sis_imports"


class SISImport(Canvas):
    def import_str(self, csv, params={}):
        """
        Imports a CSV string.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        params["import_type"] = SISImportModel.CSV_IMPORT_TYPE
        url = SIS_IMPORTS_API.format(
            self._canvas_account_id) + ".json{}".format(self._params(params))
        headers = {"Content-Type": "text/csv"}

        return SISImportModel(data=self._post_resource(url, headers, csv))

    def import_archive(self, archive, params={}):
        """
        Imports a zip archive of CSV files.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        params["import_type"] = SISImportModel.CSV_IMPORT_TYPE
        url = SIS_IMPORTS_API.format(
            self._canvas_account_id) + ".json{}".format(self._params(params))
        headers = {"Content-Type": "application/zip"}

        return SISImportModel(data=self._post_resource(url, headers, archive))

    def import_dir(self, dir_path, params={}):
        """
        Imports a directory of CSV files.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create
        """
        archive = self._build_archive(dir_path)
        return self.import_archive(archive, params)

    def get_import_status(self, sis_import):
        """
        Get the status of an already created SIS import.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.show
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        url = SIS_IMPORTS_API.format(
            self._canvas_account_id) + "/{}.json".format(sis_import.import_id)

        return SISImportModel(data=self._get_resource(url))

    def get_imports(self, params={}):
        """
        Get Canvas sis imports

        https://developerdocs.instructure.com/services/canvas/resources/sis_imports#method.sis_imports_api.index
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        url = SIS_IMPORTS_API.format(self._canvas_account_id)
        data_key = 'sis_imports'

        imports = self._get_paged_resource(
            url, params=params, data_key=data_key).get(data_key, [])

        return [SISImportModel(data=data) for data in imports]

    def get_import_errors(self, sis_import):
        """
        Get errors associated with specific Canvas import

        https://developerdocs.instructure.com/services/canvas/resources/sis_import_errors
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        url = SIS_IMPORTS_API.format(
            self._canvas_account_id) + f"/{sis_import.import_id}/errors"
        data_key = 'sis_import_errors'

        errors = self._get_resource_url(
            url, True, data_key=data_key).get(data_key, [])

        return [SISImportErrorModel(data=data) for data in errors]

    def _post_resource(self, url, headers, body):
        headers.update({"Accept": "application/json",
                        "Connection": "keep-alive"})
        response = Canvas_DAO().postURL(url, headers, body)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        response_data = json.loads(response.data)
        response_data["post_url"] = url
        response_data["post_headers"] = headers
        return response_data

    def _build_archive(self, dir_path):
        """
        Creates a zip archive from files in path.
        """
        zip_path = os.path.join(dir_path, "import.zip")
        archive = zipfile.ZipFile(zip_path, "w")

        for filename in CSV_FILES:
            filepath = os.path.join(dir_path, filename)

            if os.path.exists(filepath):
                archive.write(filepath, filename, zipfile.ZIP_DEFLATED)

        archive.close()

        with open(zip_path, "rb") as f:
            body = f.read()

        return body

    def delete_import(self, sis_import):
        """
        Abort a SIS import that has not completed.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        url = SIS_IMPORTS_API.format(
            self._canvas_account_id) + "/{}/abort".format(sis_import.import_id)

        return SISImportModel(data=self._put_resource(url))

    def delete_all_pending_imports(self):
        """
        Abort already created but not processed or processing SIS imports.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.abort_all_pending
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        url = SIS_IMPORTS_API.format(
            self._canvas_account_id) + "/abort_all_pending"

        return self._put_resource(url)
