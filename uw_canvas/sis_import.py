from uw_canvas import Canvas
from uw_canvas.models import SISImport as SISImportModel
from uw_canvas.dao import Canvas_DAO
from restclients_core.exceptions import DataFailureException
from commonconf import settings
import zipfile
import json
import os


# List of csv files determines sequence of import
CSV_FILES = ["accounts.csv", "users.csv", "terms.csv", "courses.csv",
             "sections.csv", "enrollments.csv", "xlists.csv"]


class SISImport(Canvas):
    def import_str(self, csv, params={}):
        """
        Imports a CSV string.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create
        """
        params["import_type"] = SISImportModel.CSV_IMPORT_TYPE
        url = "/api/v1/accounts/%s/sis_imports.json%s" % (
            settings.RESTCLIENTS_CANVAS_ACCOUNT_ID, self._params(params))
        headers = {"Content-Type": "text/csv"}

        data = self._post_resource(url, headers, csv)

        return self._sis_import_from_json(data)

    def import_dir(self, dir_path, params={}):
        """
        Imports a directory of CSV files.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.create
        """
        body = self._build_archive(dir_path)
        params["import_type"] = SISImportModel.CSV_IMPORT_TYPE
        url = "/api/v1/accounts/%s/sis_imports.json%s" % (
            settings.RESTCLIENTS_CANVAS_ACCOUNT_ID, self._params(params))
        headers = {"Content-Type": "application/zip"}

        data = self._post_resource(url, headers, body)

        return self._sis_import_from_json(data)

    def get_import_status(self, sis_import):
        """
        Get the status of an already created SIS import.

        https://canvas.instructure.com/doc/api/sis_imports.html#method.sis_imports_api.show
        """
        url = "/api/v1/accounts/%s/sis_imports/%s.json" % (
            settings.RESTCLIENTS_CANVAS_ACCOUNT_ID, sis_import.import_id)

        return self._sis_import_from_json(self._get_resource(url))

    def _post_resource(self, url, headers, body):
        headers.update({"Accept": "application/json",
                        "Connection": "keep-alive"})
        response = Canvas_DAO().postURL(url, headers, body)

        if not (response.status == 200 or response.status == 204):
            raise DataFailureException(url, response.status, response.data)

        return json.loads(response.data)

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

        with open(zip_path, "r") as f:
            body = f.read()

        return body

    def _sis_import_from_json(self, data):
        sis_import = SISImportModel()
        sis_import.import_id = data["id"]
        sis_import.workflow_state = data["workflow_state"]
        sis_import.progress = data.get("progress", "0")
        sis_import.processing_warnings = data.get("processing_warnings", [])
        sis_import.processing_errors = data.get("processing_errors", [])
        return sis_import
