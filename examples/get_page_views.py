from commonconf.backends import use_configparser_backend
from commonconf import settings
from dateutil.parser import parse
import argparse
import json
import os


def get_page_views(login, start, end):
    from uw_canvas.users import Users

    start_time = parse(start)
    end_time = parse(end)

    if end_time < start_time:
        raise ValueError('End date is before start date')

    canvas = Users(per_page=500)
    page_views = canvas.get_user_page_views_by_sis_login_id(
        login, start_time=start_time, end_time=end_time)

    file_name = '{}-page-views-{}-{}.json'.format(
        login, start_time.date(), end_time.date())
    with open(file_name, 'w') as outfile:
        json.dump(page_views, outfile)


if __name__ == '__main__':
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    parser = argparse.ArgumentParser()
    parser.add_argument('login', help='Login for which to get page views')
    parser.add_argument('start', help='Starting date for page views, yyyy-m-d')
    parser.add_argument('end', help='Ending date for page views, yyyy-m-d')
    args = parser.parse_args()
    get_page_views(args.login, args.start, args.end)
