# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_canvas import Canvas
from uw_canvas.models import Outcome

OUTCOMES_API = '/api/v1/outcomes/{}'


class Outcomes(Canvas):
    def get_outcome_by_id(self, outcome_id, **params):
        """
        https://canvas.instructure.com/doc/api/outcomes.html#method.outcomes_api.show
        """
        url = OUTCOMES_API.format(outcome_id)
        return Outcome(data=self._get_resource(url, params=params))
