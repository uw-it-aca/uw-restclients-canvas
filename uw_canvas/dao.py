"""
Contains Canvas DAO implementations.
"""
from restclients_core.dao import DAO, LiveDAO
from commonconf import settings
from urllib3 import PoolManager
from os.path import abspath, dirname
import os
import re


class Canvas_DAO(DAO):
    def service_name(self):
        return "canvas"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def _custom_headers(self, method, url, headers, body):
        bearer_key = self.get_service_setting("OAUTH_BEARER", "")
        return {"Authorization": "Bearer %s" % bearer_key}

    def _edit_mock_response(self, method, url, headers, body, response):
        if "POST" == method or "PUT" == method:
            if response.status != 400:
                path = "%s/resources/canvas/file%s.%s" % (
                    abspath(dirname(__file__)), url, method)

                try:
                    handle = open(path)
                    response.data = handle.read()
                    response.status = 200
                except IOError:
                    response.status = 404
        elif "DELETE" == method:
            response.status = 200


class CanvasFileDownloadLiveDAO(LiveDAO):
    def load(self, method, url, headers, body):
        # Ensure file url matches the hostname in settings,
        # workaround for Canvas bug help.instructure.com/tickets/362386
        host = self.dao.get_service_setting("HOST")
        url = re.sub(r'^https://[^/]+', host, url)
        socket_timeout = self.dao.get_service_setting("TIMEOUT", 10)
        ca_certs = self.dao.get_setting("CA_BUNDLE",
                                        "/etc/ssl/certs/ca-bundle.crt")
        pool_manager = PoolManager(
            cert_reqs="CERT_REQUIRED", ca_certs=ca_certs,
            retries=1, redirect=1, timeout=socket_timeout)

        return pool_manager.request(method, url, headers=headers)


class CanvasFileDownload_DAO(Canvas_DAO):
    def _get_live_implementation(self):
        return CanvasFileDownloadLiveDAO(self.service_name(), self)
