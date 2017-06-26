from uw_canvas.courses import Courses
from commonconf.backends import use_configparser_backend
from commonconf import settings
import os


def get_courses():
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    account_id = getattr(settings, 'RESTCLIENTS_CANVAS_ACCOUNT_ID')

    canvas = Courses()
    for course in canvas.get_courses_in_account(account_id):
        print(course.name)


if __name__ == '__main__':
    get_courses()
