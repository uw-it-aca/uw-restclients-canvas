from uw_canvas import Canvas
from uw_canvas.dao import Canvas_DAO
from restclients_core.exceptions import DataFailureException


class Analytics(Canvas):
    def get_activity_by_account(self, account_id, term_id):
        """
        Returns participation data for the given account_id and term_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_participation
        """
        url = ("/api/v1/accounts/sis_account_id:%s/analytics/"
               "terms/sis_term_id:%s/activity.json") % (account_id, term_id)
        return self._get_resource(url)

    def get_grades_by_account(self, account_id, term_id):
        """
        Returns grade data for the given account_id and term_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_grades
        """
        url = ("/api/v1/accounts/sis_account_id:%s/analytics/"
               "terms/sis_term_id:%s/grades.json") % (account_id, term_id)
        return self._get_resource(url)

    def get_statistics_by_account(self, account_id, term_id):
        """
        Returns statistics for the given account_id and term_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.department_statistics
        """
        url = ("/api/v1/accounts/sis_account_id:%s/analytics/"
               "terms/sis_term_id:%s/statistics.json") % (account_id, term_id)
        return self._get_resource(url)

    def get_activity_by_course(self, sis_course_id):
        return self.get_activity_by_sis_course_id(course_id)

    def get_activity_by_sis_course_id(self, sis_course_id):
        """
        Returns participation data for the given sis_course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_participation
        """
        url = "/api/v1/courses/%s/analytics/activity.json" % (
            self._sis_id(sis_course_id, sis_field="course"))
        return self._get_resource(url)

    def get_assignments_by_course(self, course_id):
        return self.get_assignments_by_sis_course_id(course_id)

    def get_assignments_by_sis_course_id(self, sis_course_id):
        """
        Returns assignment data for the given course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_assignments
        """
        url = "/api/v1/courses/%s/analytics/assignments.json" % (
            self._sis_id(sis_course_id, sis_field="course"))
        return self._get_resource(url)

    def get_student_summaries_by_course(self, course_id):
        return self.get_student_summaries_by_sis_course_id(course_id)

    def get_student_summaries_by_sis_course_id(self, sis_course_id):
        """
        Returns per-student data for the given course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.course_student_summaries
        """
        url = "/api/v1/courses/%s/analytics/student_summaries.json" % (
            self._sis_id(sis_course_id, sis_field="course"))
        return self._get_resource(url)

    def get_student_activity_for_course(self, user_id, course_id):
        return self.get_student_activity_for_sis_course_id_and_sis_user_id(
            self, user_id, course_id)

    def get_student_activity_for_sis_course_id_and_sis_user_id(
            self, sis_user_id, sis_course_id):
        """
        Returns student activity data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_participation
        """
        url = ("/api/v1/courses/%s/analytics/users/"
               "sis_user_id:%s/activity.json") % (
            self._sis_id(sis_course_id, sis_field="course"), sis_user_id)
        return self._get_resource(url)

    def get_student_assignments_for_course(self, user_id, course_id):
        return self.get_student_assignments_for_sis_course_id_and_sis_user_id(
            user_id, course_id)

    def get_student_assignments_for_sis_course_id_and_sis_user_id(
            self, sis_user_id, sis_course_id):
        """
        Returns student assignment data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments
        """
        url = ("/api/v1/courses/%s/analytics/"
               "users/sis_user_id:%s/assignments.json") % (
            self._sis_id(sis_course_id, sis_field="course"), sis_user_id)
        return self._get_resource(url)

    def get_student_assignments_for_sis_course_id_and_canvas_user_id(
            self, sis_course_id, user_id):
        """
        Returns student assignment data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_assignments
        """

        url = "/api/v1/courses/%s/analytics/users/%s/assignments.json" % (
            self._sis_id(sis_course_id, sis_field="course"), user_id)
        return self._get_resource(url)

    def get_student_messaging_for_course(self, user_id, course_id):
        return self.get_student_messaging_for_sis_course_id_and_sis_user_id(
            user_id, course_id)

    def get_student_messaging_for_sis_course_id_and_sis_user_id(
            self, sis_user_id, sis_course_id):
        """
        Returns student messaging data for the given user_id and course_id.

        https://canvas.instructure.com/doc/api/analytics.html#method.analytics_api.student_in_course_messaging
        """
        url = ("/api/v1/courses/%s/analytics/"
               "users/sis_user_id:%s/communication.json") % (
            self._sis_id(sis_course_id, sis_field="course"), sis_user_id)
        return self._get_resource(url)
