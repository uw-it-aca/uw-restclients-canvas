# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import Rubric

RUBRICS_API = COURSES_API + "/rubrics"


class Rubrics(Canvas):
    def get_rubrics_by_course(self, course_id, **params):
        """
        https://canvas.instructure.com/doc/api/rubrics.html#method.rubrics_api.show
        """

        rubrics = []
        url = RUBRICS_API.format(course_id)
        data = self._get_paged_resource(url, params=params,
                                        data_key='rubrics')

        for rubric in data:
            rubrics.append(Rubric(data=rubric))

        return rubrics
