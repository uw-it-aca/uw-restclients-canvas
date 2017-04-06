from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.terms import Terms


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
