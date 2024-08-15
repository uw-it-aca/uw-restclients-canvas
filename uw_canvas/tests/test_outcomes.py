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

        result = results[0]
        self.assertTrue(result.mastery)
        self.assertEqual(result.score, 1.0)
        self.assertEqual(result.possible, 1.0)
        self.assertEqual(result.percent, 1.0)
        self.assertTrue(result.hide_points)
        self.assertFalse(result.hidden)
        self.assertEqual(result.user_id, "188885")

    def test_get_outcomes_by_course(self):
        canvas = OutcomeResults()
        results, outcomes = canvas.get_outcome_results_by_course(
            "862539", params={"include": ["outcomes"]})

        self.assertEqual(len(outcomes), 6)

        outcome = outcomes[0]
        self.assertEqual(outcome.context_type, "Course")
        self.assertIsNone(outcome.vendor_guid)
        self.assertTrue(outcome.can_edit)
        self.assertEqual(outcome.points_possible, 1.0)
        self.assertEqual(outcome.mastery_points, 1.0)
        self.assertEqual(outcome.calculation_method, "latest")
        self.assertTrue(outcome.assessed)

    def test_get_outcome_groups_by_course(self):
        canvas = OutcomeResults()
        results, groups = canvas.get_outcome_results_by_course(
            "862539", params={"include": ["outcome_groups"]})

        self.assertEqual(len(groups), 2)

        group = groups[0]
        self.assertEqual(group.title, "Term 2 Milestone OSCE")
        self.assertIsNone(group.vendor_guid)
        self.assertTrue(group.can_edit)
        self.assertEqual(group.context_type, "Course")
        self.assertIsNone(group.description)
