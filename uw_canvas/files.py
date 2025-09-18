# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import File

COURSE_FILES_API = COURSES_API + "/files"


class Files(Canvas):
    def get_course_files_by_sis_id(self, sis_id, params={}):
        """
        List files for a given course sis id

        https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        return self.get_course_files(self._sis_id(sis_id, "course"), params)

    def get_course_files(self, course_id, params={}):
        """
        List files for a given course

        https://canvas.instructure.com/doc/api/files.html#method.files.api_index
        """
        url = COURSE_FILES_API.format(course_id)
        data = self._get_paged_resource(url, params=params)
        files = []
        for datum in data:
            files.append(File(data=datum))
        return files
