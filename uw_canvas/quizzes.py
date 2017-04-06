from uw_canvas import Canvas
from uw_canvas.models import Quiz
import dateutil.parser


class Quizzes(Canvas):
    def get_quizzes_by_sis_id(self, sis_id):
        """
        List quizzes for a given course sis id

        https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes_api.index
        """
        return self.get_quizzes(self._sis_id(sis_id, "course"))

    def get_quizzes(self, course_id):
        """
        List quizzes for a given course

        https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes_api.index
        """

        url = "/api/v1/courses/%s/quizzes" % course_id
        data = self._get_resource(url)
        quizzes = []
        for quiz in data:
            quiz = self._quiz_from_json(quiz)
            quizzes.append(quiz)
        return quizzes

    def _quiz_from_json(self, data):
        quiz = Quiz()
        quiz.quiz_id = data['id']
        try:
            quiz.due_at = dateutil.parser.parse(data['due_at'])
        except Exception as ex:
            quiz.due_at = None
        quiz.title = data['title']
        quiz.html_url = data['html_url']
        quiz.published = data['published']
        quiz.points_possible = data['points_possible']

        return quiz

    def get_submissions_for_sis_course_id_and_quiz_id(
            self, sis_course_id, quiz_id):
        url = "/api/v1/courses/%s/quizzes/%s/submissions" % (
            self._sis_id(sis_course_id, sis_field="course"), quiz_id)
        submissions = Canvas()._get_resource(url, data_key="quiz_submissions")

        return submissions
