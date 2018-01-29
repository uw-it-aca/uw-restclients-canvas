from commonconf import override_settings


fdao_canvas_override = override_settings(CANVAS_DAO_CLASS='Mock',
                                         CANVAS_ACCOUNT_ID=12345)
