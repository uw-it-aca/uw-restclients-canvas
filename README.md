# REST client for the Canvas LMS API

[![Build Status](https://github.com/uw-it-aca/uw-restclients-canvas/workflows/tests/badge.svg)](https://github.com/uw-it-aca/uw-restclients-canvas/actions)
[![Coverage Status](https://coveralls.io/repos/uw-it-aca/uw-restclients-canvas/badge.svg?branch=main)](https://coveralls.io/r/uw-it-aca/uw-restclients-canvas?branch=main)
[![PyPi Version](https://img.shields.io/pypi/v/uw-restclients-canvas.svg)](https://pypi.python.org/pypi/uw-restclients-canvas)
![Python versions](https://img.shields.io/badge/python-3.10-blue.svg)


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

    # Path to a CA bundle for SSL verification (PEM format)
    # If in doubt, inspect the endpoint certificate chain with something like 
    # `openssl s_client -connect canvas.test.edu:443 </dev/null`
    RESTCLIENTS_CA_BUNDLE=

See examples for usage.  Pull requests welcome.
