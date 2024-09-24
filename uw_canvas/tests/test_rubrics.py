# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.rubrics import Rubrics
from uw_canvas.models import Rubric, Criterion, Rating
import mock


@fdao_canvas_override
class CanvasTestRubrics(TestCase):
    def test_rubrics_by_course(self):
        canvas = Rubrics()
        res = canvas.get_rubrics_by_course('862539')
        rubric = res[0]

        self.assertEqual(rubric.points_possible, 0)
        self.assertEqual(rubric.title, 'Test Rubric')
        self.assertFalse(rubric.public)
        self.assertFalse(rubric.read_only)
        self.assertFalse(rubric.reusable)
        self.assertFalse(rubric.hide_score_total)
        self.assertEqual(len(rubric.criteria), 4)

        crit = rubric.criteria[3]
        self.assertEqual(crit.description, 'Assessment:')
        self.assertEqual(crit.points, 0)
        self.assertFalse(crit.criterion_use_range)
        self.assertEqual(
            crit.long_description, (
                'Starts with a summary statement followed by an assessment of '
                'how well the condition is managed.  Notes any goals or '
                'barriers identified today.'))
        self.assertEqual(crit.mastery_points, None)
        self.assertFalse(crit.ignore_for_scoring)
        self.assertEqual(len(crit.ratings), 2)

        rating = crit.ratings[1]
        self.assertEqual(rating.description, "No Marks")
        self.assertEqual(rating.points, 0)
