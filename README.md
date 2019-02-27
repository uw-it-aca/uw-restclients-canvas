# REST client for the Canvas LMS API

[![Build Status](https://api.travis-ci.org/uw-it-aca/uw-restclients-canvas.svg?branch=master)](https://travis-ci.org/uw-it-aca/uw-restclients-canvas)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/uw-restclients-canvas/badge.svg?branch=master)](https://coveralls.io/r/uw-it-aca/uw-restclients-canvas?branch=master)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-canvas.svg)](https://pypi.python.org/pypi/uw-restclients-canvas)
![Python versions](https://img.shields.io/pypi/pyversions/uw-restclients-canvas.svg)


Installation:

    pip install UW-RestClients-Canvas

To use this client, you'll need these settings in your application or script:

    # Specifies whether requests should use live or mocked resources,
    # acceptable values are 'Live' or 'Mock' (default)
    RESTCLIENTS_CANVAS_DAO_CLASS=

    # Canvas host, for example https://canvas.test.edu
    RESTCLIENTS_CANVAS_HOST=

    # Access Token for authenticating to Canvas web services
    RESTCLIENTS_CANVAS_OAUTH_BEARER=

    # Root account ID for this Canvas instance
    RESTCLIENTS_CANVAS_ACCOUNT_ID=

See examples for usage.  Pull requests welcome.
