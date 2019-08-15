from commonconf.backends import use_configparser_backend
from commonconf import settings
from datetime import datetime
import argparse
import json
import os


def get_page_views(login):
    from uw_canvas.users import Users

    start_time = datetime(2019, 1, 1)
    end_time = datetime(2019, 5, 1)

    canvas = Users(per_page=500)
    page_views = canvas.get_user_page_views_by_sis_login_id(
        login, start_time=start_time, end_time=end_time)

    with open('data.json', 'w') as outfile:
        json.dump(page_views, outfile)


if __name__ == '__main__':
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    parser = argparse.ArgumentParser()
    parser.add_argument('login', help='Login for which to get page views')
    args = parser.parse_args()
    get_page_views(args.login)
