# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas


class Analytics(Canvas):

    def get_activity_by_account(self, account_id, term_id, **params):
        """
        Returns participation data for the given account_id and term_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation
        """
        url = ("/api/v1/accounts/%s/analytics/"
               "terms/%s/activity.json") % (
                self._sis_id(account_id, sis_field="account"),
                self._sis_id(term_id, sis_field="term"))
        return self._get_resource(url, params=params)

    def get_grades_by_account(self, account_id, term_id, **params):
        """
        Returns grade data for the given account_id and term_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades
        """
        url = ("/api/v1/accounts/%s/analytics/"
               "terms/%s/grades.json") % (
                self._sis_id(account_id, sis_field="account"),
                self._sis_id(term_id, sis_field="term"))
        return self._get_resource(url, params=params)

    def get_statistics_by_account(self, account_id, term_id, **params):
        """
        Returns statistics for the given account_id and term_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics
        """
        url = ("/api/v1/accounts/%s/analytics/"
               "terms/%s/statistics.json") % (
                self._sis_id(account_id, sis_field="account"),
                self._sis_id(term_id, sis_field="term"))
        return self._get_resource(url, params=params)

    def get_activity_by_sis_course_id(self, sis_course_id, **params):
        return self.get_activity_by_course(
            self._sis_id(sis_course_id, sis_field="course"),
            **params)

    def get_activity_by_course(self, course_id, **params):
        """
        Returns participation data for the given course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation
        """
        url = "/api/v1/courses/%s/analytics/activity.json" % (course_id)
        return self._get_resource(url, params=params)

    def get_assignments_by_course(self, course_id, **params):
        return self.get_assignments_by_sis_course_id(course_id, **params)

    def get_assignments_by_sis_course_id(self, sis_course_id, **params):
        """
        Returns assignment data for the given course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_assignments
        """
        url = "/api/v1/courses/%s/analytics/assignments.json" % (
            self._sis_id(sis_course_id, sis_field="course"))
        return self._get_resource(url, params=params)

    def get_student_summaries_by_sis_course_id(self, sis_course_id, **params):
        return self.get_student_summaries_by_course(
            self._sis_id(sis_course_id, sis_field="course"),
            **params)

    def get_student_summaries_by_course(self, course_id, **params):
        """
        Returns per-student data for the given course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_student_summaries
        """
        url = "/api/v1/courses/%s/analytics/student_summaries.json" % (
            course_id)
        return self._get_resource(url, params=params)

    def get_student_activity_for_sis_course_id_and_sis_user_id(
            self, sis_user_id, sis_course_id, **params):
        return self.get_student_activity_for_course(
            self._sis_id(sis_user_id, sis_field="user"),
            self._sis_id(sis_course_id, sis_field="course"),
            **params)

    def get_student_activity_for_course(self, user_id, course_id, **params):
        """
        Returns student activity data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation
        """
        url = ("/api/v1/courses/%s/analytics/users/"
               "%s/activity.json") % (course_id, user_id)
        return self._get_resource(url, params=params)

    def get_student_assignments_for_sis_course_id_and_sis_user_id(
            self, sis_user_id, sis_course_id, **params):
        return self.get_student_assignments_for_course(
            self._sis_id(sis_user_id, sis_field="user"),
            self._sis_id(sis_course_id, sis_field="course"),
            **params)

    def get_student_assignments_for_sis_course_id_and_canvas_user_id(
            self, user_id, sis_course_id, **params):
        return self.get_student_assignments_for_course(
            user_id,
            self._sis_id(sis_course_id, sis_field="course"),
            **params)

    def get_student_assignments_for_course_id_and_sis_user_id(
            self, sis_user_id, course_id, **params):
        return self.get_student_assignments_for_course(
            self._sis_id(sis_user_id, sis_field="user"),
            course_id,
            **params)

    def get_student_assignments_for_course(self, user_id, course_id, **params):
        """
        Returns student assignment data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments
        """
        url = ("/api/v1/courses/%s/analytics/"
               "users/%s/assignments.json") % (course_id, user_id)
        return self._get_resource(url, params=params)

    def get_student_messaging_for_sis_course_id_and_sis_user_id(
            self, sis_user_id, sis_course_id, **params):
        self.get_student_messaging_for_course(
            self._sis_id(sis_user_id, sis_field="user"),
            self._sis_id(sis_course_id, sis_field="course"),
            **params)

    def get_student_messaging_for_course(self, user_id, course_id, **params):
        """
        Returns student messaging data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging
        """
        url = ("/api/v1/courses/%s/analytics/"
               "users/%s/communication.json") % (course_id, user_id)
        return self._get_resource(url, params=params)
