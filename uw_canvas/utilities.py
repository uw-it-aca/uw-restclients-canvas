from commonconf import override_settings


fdao_canvas_override = override_settings(RESTCLIENTS_CANVAS_DAO_CLASS='Mock')
ldao_canvas_override = override_settings(RESTCLIENTS_CANVAS_DAO_CLASS='Live')
