from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.reports import Reports, ReportFailureException
from uw_canvas.models import Report, ReportType
import mock


@fdao_canvas_override
class CanvasTestReports(TestCase):
    @mock.patch.object(Reports, '_get_resource')
    def test_get_available_reports(self, mock_get):
        canvas = Reports()
        canvas.get_available_reports('12345')
        mock_get.assert_called_with('/api/v1/accounts/12345/reports')

    @mock.patch.object(Reports, '_get_resource')
    def test_get_reports_by_type(self, mock_get):
        canvas = Reports()
        canvas.get_reports_by_type('12345', 'some_type')
        mock_get.assert_called_with('/api/v1/accounts/12345/reports/some_type')

    @mock.patch.object(Reports, '_post_resource')
    def test_create_report(self, mock_post):
        canvas = Reports()
        canvas.create_report('some_type', '12345')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/some_type', {'parameters': {}})

    @mock.patch.object(Reports, '_post_resource')
    def test_create_course_provisioning_report(self, mock_post):
        canvas = Reports()
        canvas.create_course_provisioning_report('12345')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/provisioning_csv',
            {'parameters': {'courses': True}})

        # With a term_id
        canvas.create_course_provisioning_report('12345',
                                                 term_id='2013-spring')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/provisioning_csv',
            {'parameters': {'courses': True,
                            'enrollment_term_id': '2013-spring'}})

    @mock.patch.object(Reports, '_post_resource')
    def test_create_enrollments_provisioning_report(self, mock_post):
        canvas = Reports()
        canvas.create_enrollments_provisioning_report('12345')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/provisioning_csv',
            {'parameters': {'enrollments': True}})

    @mock.patch.object(Reports, '_post_resource')
    def test_create_user_provisioning_report(self, mock_post):
        canvas = Reports()
        canvas.create_user_provisioning_report('12345')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/provisioning_csv',
            {'parameters': {'users': True}})

    @mock.patch.object(Reports, '_post_resource')
    def test_create_xlist_provisioning_report(self, mock_post):
        canvas = Reports()
        canvas.create_xlist_provisioning_report('12345')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/provisioning_csv',
            {'parameters': {'xlist': True}})

    @mock.patch.object(Reports, '_post_resource')
    def test_create_course_sis_export_report(self, mock_post):
        canvas = Reports()
        canvas.create_course_sis_export_report('12345')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/sis_export_csv',
            {'parameters': {'courses': True}})

    @mock.patch.object(Reports, '_post_resource')
    def test_create_unused_courses_report(self, mock_post):
        canvas = Reports()
        canvas.create_unused_courses_report('12345', term_id='2015-summer')
        mock_post.assert_called_with(
            '/api/v1/accounts/12345/reports/unused_courses_csv',
            {'parameters': {'enrollment_term_id': '2015-summer'}})

    def test_get_report_status(self):
        canvas = Reports()

        # Bad report, missing account_id
        report = Report(report_id=1)
        self.assertRaises(
            ReportFailureException, canvas.get_report_status, report)

        report = canvas.get_report_status(self._setup_report())
        self.assertEquals(report.report_id, 1)
        self.assertEquals(report.status, "complete")
        self.assertEquals(report.progress, "100")

    @mock.patch.object(Reports, '_delete_resource')
    def test_delete_report(self, mock_delete):
        canvas = Reports()
        canvas.delete_report(self._setup_report())
        mock_delete.assert_called_with(
            '/api/v1/accounts/12345/reports/some_type/1')

    def _setup_report(self):
        return Report(account_id='12345', report_id=1, type='some_type')
