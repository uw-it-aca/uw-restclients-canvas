# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.dao import CanvasFileDownload_DAO
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.models import Report, ReportType, Attachment
from restclients_core.exceptions import DataFailureException
from commonconf import settings
from time import sleep
import re


class ReportFailureException(Exception):
    """
    This exception means there was an error fetching report data.
    """
    def __init__(self, report):
        self.report = report

    def __str__(self):
        return ("Error fetching report {}".format(self.report.report_id))


class Reports(Canvas):
    def get_available_reports(self, account_id):
        """
        Returns the list of reports for the canvas account id.

        https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.available_reports
        """
        url = ACCOUNTS_API.format(account_id) + "/reports"

        report_types = []
        for datum in self._get_resource(url):
            report_types.append(ReportType(data=datum, account_id=account_id))
        return report_types

    def get_reports_by_type(self, account_id, report_type):
        """
        Shows all reports of the passed report_type that have been run
        for the canvas account id.

        https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.index
        """
        url = ACCOUNTS_API.format(account_id) + "/reports/{}".format(
            report_type)

        reports = []
        for datum in self._get_resource(url):
            datum["account_id"] = account_id
            reports.append(Report(data=datum))

        return reports

    def create_report(self, report_type, account_id, term_id=None, params={}):
        """
        Generates a report instance for the canvas account id.

        https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.create
        """
        if term_id is not None:
            params["enrollment_term_id"] = term_id

        url = ACCOUNTS_API.format(account_id) + "/reports/{}".format(
            report_type)
        body = {"parameters": params}

        data = self._post_resource(url, body)
        data["account_id"] = account_id
        return Report(data=data)

    def create_course_provisioning_report(self, account_id, term_id=None,
                                          params={}):
        """
        Convenience method for create_report, for creating a course
        provisioning report.
        """
        params["courses"] = True
        return self.create_report(ReportType.PROVISIONING, account_id, term_id,
                                  params)

    def create_enrollments_provisioning_report(self, account_id, term_id=None,
                                               params={}):
        """
        Convenience method for create_report, for creating an enrollment
        provisioning report.
        """
        params["enrollments"] = True
        return self.create_report(ReportType.PROVISIONING, account_id, term_id,
                                  params)

    def create_user_provisioning_report(self, account_id, term_id=None,
                                        params={}):
        """
        Convenience method for create_report, for creating a user
        provisioning report.
        """
        params["users"] = True
        return self.create_report(ReportType.PROVISIONING, account_id, term_id,
                                  params)

    def create_xlist_provisioning_report(self, account_id, term_id=None,
                                         params={}):
        """
        Convenience method for create_report, for creating a crosslist
        provisioning report.
        """
        params["xlist"] = True
        return self.create_report(ReportType.PROVISIONING, account_id, term_id,
                                  params)

    def create_course_sis_export_report(self, account_id, term_id=None,
                                        params={}):
        """
        Convenience method for create_report, for creating a course sis export
        report.
        """
        params["courses"] = True
        return self.create_report(ReportType.SIS_EXPORT, account_id, term_id,
                                  params)

    def create_unused_courses_report(self, account_id, term_id=None):
        """
        Convenience method for create_report, for creating an unused courses
        report.
        """
        return self.create_report(ReportType.UNUSED_COURSES, account_id,
                                  term_id)

    def get_report_data(self, report):
        """
        Returns a completed report as a list of csv strings.
        """
        if report.report_id is None or report.status is None:
            raise ReportFailureException(report)

        interval = getattr(settings, 'CANVAS_REPORT_POLLING_INTERVAL', 5)
        while report.status != "complete":
            if report.status == "error":
                raise ReportFailureException(report)
            sleep(interval)
            report = self.get_report_status(report)

        if report.attachment is None or report.attachment.url is None:
            return

        data = self._get_report_file(report.attachment.url)

        return data.split("\n")

    def get_report_status(self, report):
        """
        Returns the status of a report.

        https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.show
        """
        if (report.account_id is None or report.type is None or
                report.report_id is None):
            raise ReportFailureException(report)

        url = ACCOUNTS_API.format(report.account_id) + "/reports/{}/{}".format(
            report.type, report.report_id)

        data = self._get_resource(url)
        data["account_id"] = report.account_id
        return Report(data=data)

    def delete_report(self, report):
        """
        Deletes a generated report instance.

        https://canvas.instructure.com/doc/api/account_reports.html#method.account_reports.destroy
        """
        url = ACCOUNTS_API.format(report.account_id) + "/reports/{}/{}".format(
            report.type, report.report_id)

        response = self._delete_resource(url)
        return True

    def _get_report_file(self, url):
        response = CanvasFileDownload_DAO().getURL(url)

        if response.status != 200:
            raise DataFailureException(url, response.status, response.data)

        return response.data.decode("utf-8")
