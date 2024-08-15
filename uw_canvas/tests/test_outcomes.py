# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.outcome_results import OutcomeResults
from uw_canvas.models import Outcome, OutcomeGroup, OutcomeResult
import mock


@fdao_canvas_override
class CanvasTestOutcomes(TestCase):
    def test_get_outcome_results_by_course(self):
        canvas = OutcomeResults()
        results = canvas.get_outcome_results_by_course("862539")
        self.assertEqual(len(results), 10)

        res1 = results[0]
        self.assertTrue(res1.mastery)
        self.assertEqual(res1.score, 1.0)
        self.assertEqual(res1.possible, 1.0)
        self.assertEqual(res1.percent, 1.0)
        self.assertTrue(res1.hide_points)
        self.assertFalse(res1.hidden)
        self.assertEqual(res1.user_id, "188885")
