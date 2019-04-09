from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.terms import Terms
from uw_canvas import MissingAccountID
import mock


class CanvasTestTermsMissingAccount(TestCase):
    def test_get_all_terms(self):
        canvas = Terms()
        self.assertRaises(MissingAccountID, canvas.get_all_terms)


@fdao_canvas_override
class CanvasTestTerms(TestCase):
    def test_get_all_terms(self):
        canvas = Terms()

        terms = canvas.get_all_terms()

        self.assertEquals(len(terms), 16)

    def test_get_term_by_sis_id(self):
        canvas = Terms()

        sis_term_id = "2013-summer"

        term = canvas.get_term_by_sis_id(sis_term_id)

        self.assertEquals(term.term_id, 3845, "Has proper term id")
        self.assertEquals(term.name, "Summer 2013", "Has proper name")
        self.assertEquals(term.sis_term_id, sis_term_id, "Has proper sis id")
        self.assertEquals(term.workflow_state, "active")
        self.assertEquals(str(term.start_at), "2013-06-23 07:00:00+00:00")
        self.assertEquals(str(term.end_at), "2013-08-22 07:00:00+00:00")

    @mock.patch.object(Terms, '_put_resource')
    def test_update_term_overrides(self, mock_update):
        mock_update.return_value = None
        canvas = Terms()

        canvas.update_term_overrides("2013-spring", overrides={
            "StudentEnrollment": {"start_at": "2013-01-07T08:00:00-05:00",
                                  "end_at": "2013-05-14T05:00:00-04:0"}})
        mock_update.assert_called_with(
            '/api/v1/accounts/12345/terms/sis_term_id%3A2013-spring', {
                'enrollment_term': {
                    'overrides': {'StudentEnrollment': {
                        'start_at': '2013-01-07T08:00:00-05:00',
                        'end_at': '2013-05-14T05:00:00-04:0'}}}})
