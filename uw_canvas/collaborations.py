# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import Collaboration

COLLABORATIONS_API = COURSES_API + "/collaborations"


class Collaborations(Canvas):
    def get_collaborations_for_course(self, course_id, **params):
        """
        List collaborations for a given course

        https://canvas.instructure.com/doc/api/collaborations.html#method.collaborations.api_index
        """
        url = COLLABORATIONS_API.format(course_id)
        data = self._get_paged_resource(url, params=params)
        collaborations = []
        for datum in data:
            collaborations.append(Collaboration(data=datum))
        return collaborations
