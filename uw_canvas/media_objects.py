# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import MediaObject

MEDIA_OBJECT_API = COURSES_API + "/media_objects"


class MediaObjects(Canvas):
    def get_media_objects_by_course_id(self, course_id, params={}):
        """
        Return course media objects for given canvas course id.

        https://canvas.instructure.com/doc/api/media_objects.html#method.media_objects.index
        """
        url = MEDIA_OBJECT_API.format(course_id)
        data = self._get_paged_resource(url, params=params)
        media_objects = []
        for datum in data:
            media_objects.append(MediaObject(data=datum))
        return media_objects

    def get_media_objects_by_course_sis_id(self, sis_course_id, params={}):
        """
        Return course media objects for given sis id.
        """
        return self.get_media_objects_by_course_id(
            self._sis_id(sis_course_id, sis_field="course"), params)
