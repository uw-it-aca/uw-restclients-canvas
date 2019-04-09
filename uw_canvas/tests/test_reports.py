from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.reports import Reports, ReportFailureException
from uw_canvas.models import Report, ReportType
import mock


@fdao_canvas_override
class CanvasTestReports(TestCase):
    def setUp(self):
        self.attachment_json_data = {
            "id": "11",
            "filename": "test.csv",
            "display_name": "Test",
            "content-type": "text/csv",
            "url": "https://test.canvas.edu/...",
            "size": "1024",
        }

        self.report_json_data = {
            "id": "1",
            "account_id": "12345",
            "report": "some_type",
            "file_url": None,
            "status": "complete",
            "progress": "100",
            "parameters": {},
            "attachment": self.attachment_json_data,
        }

        self.report_type_json_data = {
            "report": "sis_import",
            "title": "Report Title",
            "parameters": {},
            "last_run": self.report_json_data,
        }

    @mock.patch.object(Reports, '_get_resource')
    def test_get_available_reports(self, mock_get):
        mock_get.return_value = [self.report_type_json_data]
        canvas = Reports()
        ret = canvas.get_available_reports('12345')

        mock_get.assert_called_with('/api/v1/accounts/12345/reports')

        report = ret[0]
        self.assertEqual(report.name, self.report_type_json_data["report"])
        self.assertEqual(report.title, self.report_type_json_data["title"])
        self.assertEqual(report.last_run.type, self.report_json_data["report"])
        self.assertEqual(report.last_run.account_id, '12345')

    @mock.patch.object(Reports, '_get_resource')
    def test_get_reports_by_type(self, mock_get):
        mock_get.return_value = [self.report_json_data]
        canvas = Reports()
        ret = canvas.get_reports_by_type('12345', 'sis_import')
        mock_get.assert_called_with(
            '/api/v1/accounts/12345/reports/sis_import')

        report = ret[0]
        self.assertEqual(report.type, self.report_json_data["report"])
        self.assertEqual(report.account_id, '12345')

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

        report = Report(data=self.report_json_data)
        report = canvas.get_report_status(report)
        self.assertEquals(report.report_id, 1)
        self.assertEquals(report.status, "complete")
        self.assertEquals(report.progress, "100")

    @mock.patch.object(Reports, '_get_report_file')
    def test_get_report_data(self, mock_get):
        mock_get.return_value = "a\nb\nc\nd\ne"
        canvas = Reports()

        report = Report(report_id=1)
        self.assertRaises(
            ReportFailureException, canvas.get_report_data, report)

        report = Report(data=self.report_json_data)
        self.assertEqual(canvas.get_report_data(report),
                         ['a', 'b', 'c', 'd', 'e'])

    @mock.patch.object(Reports, '_delete_resource')
    def test_delete_report(self, mock_delete):
        canvas = Reports()

        report = Report(data=self.report_json_data)
        canvas.delete_report(report)
        mock_delete.assert_called_with(
            '/api/v1/accounts/12345/reports/some_type/1')
