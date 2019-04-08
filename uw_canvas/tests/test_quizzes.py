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
        self.assertEquals(sub.quiz_id, 762037, "Has correct quiz id")
        self.assertEquals(sub.published, True, "Is published")
        self.assertEquals(sub.due_at.day, 1, "due at datetime")

    def test_quizzes_by_sis_id(self):
        canvas = Quizzes()
        submissions = canvas.get_quizzes_by_sis_id("2013-autumn-PHYS-248-A")
        self.assertEquals(len(submissions), 1, "Submission Count")

    def test_quiz_without_due_date(self):
        quiz = Quiz(data={
            "id": "1",
            "title": "title",
            "html_url": "http://...",
            "published": False,
            "points_possible": 0,
        })

        self.assertEquals(quiz.title, "title")
        self.assertEquals(quiz.due_at, None)
