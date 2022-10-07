# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas, MissingAccountID
from uw_canvas.accounts import Accounts, ACCOUNTS_API
from uw_canvas.courses import COURSES_API
from uw_canvas.models import GradingStandard
from restclients_core.exceptions import DataFailureException


class GradingStandards(Canvas):
    def get_grading_standard_for_account(
            self, account_id, grading_standard_id):
        """
        Get a single grading standard in account context.
        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show
        """
        url = ACCOUNTS_API.format(account_id) + "/grading_standards/{}".format(
            grading_standard_id)
        return GradingStandard(data=self._get_resource(url))

    def find_grading_standard_for_account(
            self, account_id, grading_standard_id):
        """
        Get a single grading standard in account context, searching ancestor
        accounts if necessary.
        """
        if not self._canvas_account_id:
            raise MissingAccountID()

        acc = Accounts()
        while account_id is not None:
            try:
                return self.get_grading_standard_for_account(
                    account_id, grading_standard_id)
            except DataFailureException as ex:
                if ex.status == 404 and account_id != self._canvas_account_id:
                    account_id = acc.get_account(account_id).parent_account_id
                    continue
                raise

    def get_grading_standard_for_course(self, course_id, grading_standard_id):
        """
        Get a single grading standard in course context.
        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_show
        """
        url = COURSES_API.format(course_id) + "/grading_standards/{}".format(
            grading_standard_id)
        return GradingStandard(data=self._get_resource(url))

    def get_grading_standards_for_course(self, course_id):
        """
        List the grading standards available to a course
        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        url = COURSES_API.format(course_id) + "/grading_standards"

        standards = []
        for data in self._get_paged_resource(url):
            standards.append(GradingStandard(data=data))
        return standards

    def create_grading_standard_for_course(self, course_id, name,
                                           grading_scheme, creator):
        """
        Create a new grading standard for the passed course.

        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create
        """
        url = COURSES_API.format(course_id) + "/grading_standards"
        body = {
            "title": name,
            "grading_scheme_entry": grading_scheme,
            "as_user_id": creator
        }

        return GradingStandard(data=self._post_resource(url, body))
