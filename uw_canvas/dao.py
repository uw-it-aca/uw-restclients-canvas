"""
Contains Canvas DAO implementations.
"""
from restclients_core.dao import DAO, LiveDAO
from commonconf import settings
from urllib3 import PoolManager
from urllib3.util.retry import Retry
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


class CanvasFileDownload_DAO(DAO):
    def service_name(self):
        return "canvas"

    def _get_live_implementation(self):
        return CanvasFileDownloadLiveDAO(self.service_name(), self)


class CanvasFileDownloadLiveDAO(LiveDAO):
    def load(self, method, url, headers, body):
        # Ensure file url matches the hostname in settings,
        # to avoid mixing Canvas prod/test/beta hosts
        host = self.dao.get_service_setting("HOST")
        url = re.sub(r'^https://[^/]+', host, url)
        pool = self.get_pool()
        return pool.urlopen(method, url, headers=headers)

    def get_pool(self):
        return self.create_pool()

    def create_pool(self):
        # Use a PoolManager to allow redirects to other hosts
        max_pool_size = self.dao.get_service_setting("POOL_SIZE", 10)
        socket_timeout = self.dao.get_service_setting("TIMEOUT", 10)
        ca_certs = self.dao.get_setting("CA_BUNDLE",
                                        "/etc/ssl/certs/ca-bundle.crt")

        return PoolManager(
            cert_reqs="CERT_REQUIRED", ca_certs=ca_certs,
            timeout=socket_timeout, maxsize=max_pool_size, block=True,
            retries=Retry(total=1, connect=0, read=0, redirect=1))
