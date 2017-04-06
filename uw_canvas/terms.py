from uw_canvas import Canvas
from uw_canvas.models import CanvasTerm
from commonconf import settings
import dateutil.parser


class Terms(Canvas):
    def get_all_terms(self):
        """
        Return all of the terms in the account.
        https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.index
        """
        params = {"workflow_state": 'all', 'per_page': 500}
        account_id = getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID')
        url = '/api/v1/accounts/%s/terms' % account_id
        data_key = 'enrollment_terms'

        terms = []
        response = self._get_paged_resource(url, params, data_key)
        for data in response[data_key]:
            terms.append(self._term_from_json(data))
        return terms

    def get_term_by_sis_id(self, sis_term_id):
        """
        Return a term resource for the passed SIS ID.
        """
        for term in self.get_all_terms():
            if term.sis_term_id == sis_term_id:
                return term

    def update_term_overrides(self, sis_term_id, overrides={}):
        """
        Update an existing enrollment term for the passed SIS ID.
        https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms.update
        """
        account_id = getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID')
        url = '/api/v1/accounts/%s/terms/%s' % (
            account_id, self._sis_id(sis_term_id, sis_field='term'))
        body = {'enrollment_term': {'overrides': overrides}}
        return self._term_from_json(self._put_resource(url, body))

    def _term_from_json(self, data):
        term = CanvasTerm()
        term.term_id = data.get('id')
        term.sis_term_id = data.get('sis_term_id')
        term.name = data.get('name')
        term.workflow_state = data.get('workflow_state')
        if 'start_at' in data and data['start_at']:
            term.start_at = dateutil.parser.parse(data['start_at'])
        if 'end_at' in data and data['end_at']:
            term.end_at = dateutil.parser.parse(data['end_at'])
        term.overrides = data.get('overrides', {})
        return term
