# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.quizzes import Quizzes
from uw_canvas.models import Quiz


@fdao_canvas_override
class CanvasTestQuizzes(TestCase):
    def test_quizzes_by_course_id(self):
        canvas = Quizzes()
        submissions = canvas.get_quizzes("862539")

        sub = submissions[0]
        self.assertEqual(sub.quiz_id, 762037, "Has correct quiz id")
        self.assertEqual(sub.published, True, "Is published")
        self.assertEqual(sub.due_at.day, 1, "due at datetime")

    def test_quizzes_by_sis_id(self):
        canvas = Quizzes()
        submissions = canvas.get_quizzes_by_sis_id("2013-autumn-PHYS-248-A")
        self.assertEqual(len(submissions), 1, "Submission Count")

    def test_quiz_without_due_date(self):
        quiz = Quiz(data={
            "id": "1",
            "title": "title",
            "html_url": "http://...",
            "published": False,
            "points_possible": 0,
        })

        self.assertEqual(quiz.title, "title")
        self.assertEqual(quiz.due_at, None)
