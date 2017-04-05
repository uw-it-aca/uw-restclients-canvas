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
