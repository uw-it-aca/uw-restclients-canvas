from uw_canvas import Canvas, MissingAccountID
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.models import CanvasTerm


class Terms(Canvas):
    def get_all_terms(self):
        """
        Return all of the terms in the account.
        https://canvas.instructure.com/doc/api/enrollment_terms.html#method.terms_api.index
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        params = {"workflow_state": 'all', 'per_page': 500}
        url = ACCOUNTS_API.format(self._canvas_account_id) + "/terms"
        data_key = 'enrollment_terms'

        terms = []
        response = self._get_paged_resource(url, params, data_key)
        for data in response[data_key]:
            terms.append(CanvasTerm(data=data))
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
        if not self._canvas_account_id:
            raise MissingAccountID()

        url = ACCOUNTS_API.format(
            self._canvas_account_id) + "/terms/{}".format(
                self._sis_id(sis_term_id, sis_field='term'))

        body = {'enrollment_term': {'overrides': overrides}}
        return CanvasTerm(data=self._put_resource(url, body))
