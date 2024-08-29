# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import OutcomeGroup

OUTCOME_GROUPS_API = COURSES_API + "/outcome_groups"
OUTCOME_LIST_API = OUTCOME_GROUPS_API + "/{}/outcomes"


class OutcomeGroups(Canvas):
    def get_outcome_groups_by_course(self, course_id, **params):
        """
        https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.index
        """
        url = OUTCOME_GROUPS_API.format(course_id)
        outcome_groups = []
        data = self._get_paged_resource(url, params=params,
                                        data_key='outcome_groups')

        for outcome_group in data:
            outcome_groups.append(OutcomeGroup(data=outcome_group))

        return outcome_groups

    # Returns a list of the ID's of the outcomes associated with this
    # course and group.
    def get_outcome_list_by_course_and_group(self, course_id, group_id,
                                             **params):
        """
        https://canvas.instructure.com/doc/api/outcome_groups.html#method.outcome_groups_api.outcomes
        """
        url = OUTCOME_LIST_API.format(course_id, group_id)
        outcome_list = []
        data = self._get_paged_resource(url, params=params,
                                        data_key='outcome_list')

        for datum in data:
            outcome_list.append(datum['outcome']['id'])

        return outcome_list
