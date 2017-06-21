from uw_canvas.terms import Terms
from commonconf.backends import use_configparser_backend
import os


def get_all_terms():
    settings_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                 'settings.cfg')
    use_configparser_backend(settings_path, 'Canvas')

    canvas = Terms()
    for term in canvas.get_all_terms():
        print term.name


if __name__ == '__main__':
    get_all_terms()
