import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/uw-restclients-canvas>`_.
"""

version_path = 'uw_canvas/VERSION'
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='UW-RestClients-Canvas',
    version=VERSION,
    packages=['uw_canvas'],
    author='UW-IT Student & Educational Technology Services',
    author_email='aca-it@uw.edu',
    include_package_data=True,
    install_requires=['uw-restclients-core',
                      'python-dateutil',
                      'mock',
                     ],
    license='Apache License, Version 2.0',
    description=('A library for connecting to the Canvas LMS API'),
    long_description=README,
    url='https://github.com/uw-it-aca/uw-restclients-canvas',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
