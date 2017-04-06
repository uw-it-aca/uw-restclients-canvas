# This is just a test runner for coverage
from commonconf.backends import use_configparser_backend
from os.path import abspath, dirname
import os


if __name__ == '__main__':
    path = abspath(os.path.join(dirname(__file__),
                                "..", "travis-ci", "test.conf"))
    use_configparser_backend(path, 'Canvas')

    from nose2 import discover
    discover()
