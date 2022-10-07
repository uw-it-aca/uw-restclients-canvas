# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import Quiz

QUIZZES_API = COURSES_API + "/quizzes"


class Quizzes(Canvas):
    def get_quizzes_by_sis_id(self, sis_id):
        """
        List quizzes for a given course sis id

        https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes_api.index
        """
        return self.get_quizzes(self._sis_id(sis_id, "course"))

    def get_quizzes(self, course_id, **params):
        """
        List quizzes for a given course

        https://canvas.instructure.com/doc/api/quizzes.html#method.quizzes_api.index
        """
        url = QUIZZES_API.format(course_id)
        data = self._get_paged_resource(url, params=params)
        quizzes = []
        for datum in data:
            quizzes.append(Quiz(data=datum))
        return quizzes

    def get_submissions_for_sis_course_id_and_quiz_id(
            self, sis_course_id, quiz_id, **params):
        course_id = self._sis_id(sis_course_id, sis_field="course")
        url = QUIZZES_API.format(course_id) + "/{}/submissions".format(quiz_id)
        return Canvas()._get_paged_resource(
            url, params=params, data_key="quiz_submissions")
