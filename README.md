# uw-restclients-canvas
REST client for the Canvas LMS API

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
