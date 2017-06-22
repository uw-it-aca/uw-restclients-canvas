from uw_canvas.terms import Terms
from uw_canvas.reports import Reports
from commonconf.backends import use_configparser_backend
from commonconf import settings
import os


def create_report():
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    account_id = getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID')
    term = Terms().get_term_by_sis_id('2013-autumn')

    report_client = Reports()
    report = report_client.create_course_sis_export_report(
        account_id, term.term_id)

    print('Report created. Report ID: %s, progress: %s%%' % (
        report.report_id, report.progress))

    # Fetch the report data.  This method will poll Canvas until the
    # report has been generated, and then download the data file
    data = report_client.get_report_data(report)


    # Do something with the data...


    # Delete the report
    report_client.delete_report(report)


if __name__ == '__main__':
    create_report()
