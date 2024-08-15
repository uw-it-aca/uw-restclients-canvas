# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import Outcome, OutcomeGroup, OutcomeResult

OUTCOMES_API = COURSES_API + "/outcome_results"


class OutcomeResults(Canvas):
    def get_outcome_results_by_course(self, course_id, params={}):
        """
        https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.index
        """
        url = OUTCOMES_API.format(course_id)
        data = self._get_paged_resource(url, params=params,
                                        data_key='outcome_results')

        outcome_results = []
        for outcome_result in data['outcome_results']:
            outcome_results.append(OutcomeResult(data=outcome_result))

        ret = [outcome_results]
        if 'linked' in data:
            outcome_groups = []
            outcomes = []

            if 'outcomes' in data['linked']:
                for outcome in data['linked']['outcomes']:
                    outcomes.append(Outcome(data=outcome))
                ret.append(outcomes)

            if 'outcome_groups' in data['linked']:
                for outcome_group in data['linked']['outcome_groups']:
                    outcome_groups.append(OutcomeGroup(data=outcome_group))
                ret.append(outcome_groups)

        return outcome_results if (len(ret) == 1) else tuple(ret)
