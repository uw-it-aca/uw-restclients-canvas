from commonconf import override_settings


fdao_canvas_override = override_settings(RESTCLIENTS_CANVAS_DAO_CLASS='Mock',
                                         RESTCLIENTS_CANVAS_ACCOUNT_ID=12345,
                                         CANVAS_REPORT_POLLING_INTERVAL=0.001)
