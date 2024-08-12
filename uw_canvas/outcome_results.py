from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import OutcomeResult
from uw_canvas.models import Outcome
from uw_canvas.models import OutcomeGroup

OUTCOMES_API = COURSES_API + "//outcome_results"


class OutcomeResults(Canvas):
    def get_outcome_results_by_course(self, course_id, params={}):
        """
        https://canvas.instructure.com/doc/api/outcome_results.html#method.outcome_results.index
        """
        url = OUTCOMES_API.format(course_id)

        outcome_results = []
        data = self._get_paged_resource(url, params=params,
                                        data_key='outcome_results')

        if 'linked' in data:
            if 'outcomes' in data['linked']:
                outcomes = []
                for outcome in data['linked']['outcomes']:
                    outcomes.append(Outcome(data=outcome))
            if 'outcome_groups' in data['linked']:
                outcome_groups = []
                for outcome_group in data['linked']['outcome_groups']:
                    outcome_groups.append(OutcomeGroup(data=outcome_group))

        for outcome_result in data['outcome_results']:
            outcome_results.append(OutcomeResult(data=outcome_result))

        if 'linked' in data:
            if ('outcomes' in data['linked'] and
                    'outcome_groups' in data['linked']):
                return outcome_results, outcomes, outcome_groups
            elif ('outcomes' in data['linked'] and
                  'outcome_groups' not in data['linked']):
                return outcome_results, outcomes
            elif ('outcomes' not in data['linked'] and
                  'outcome_groups' in data['linked']):
                return outcome_results, outcome_groups
            else:
                return outcome_results
        else:
            return outcome_results
