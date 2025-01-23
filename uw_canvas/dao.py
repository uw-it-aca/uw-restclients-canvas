# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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
    def __init__(self, *args, **kwargs):
        self.canvas_api_host = kwargs.get("canvas_api_host")
        super(Canvas_DAO, self).__init__()

    def service_name(self):
        return "canvas"

    def service_mock_paths(self):
        return [abspath(os.path.join(dirname(__file__), "resources"))]

    def get_service_setting(self, key, default=None):
        if key == "HOST" and self.canvas_api_host:
            return self.canvas_api_host

        return super(Canvas_DAO, self).get_service_setting(key, default)

    def _custom_headers(self, method, url, headers, body):
        bearer_key = self.get_service_setting("OAUTH_BEARER", "")
        return {"Authorization": "Bearer {}".format(bearer_key)}

    def _edit_mock_response(self, method, url, headers, body, response):
        if "POST" == method or "PUT" == method:
            if response.status != 400:
                path = "{path}/resources/canvas/file{url}.{method}".format(
                    path=abspath(dirname(__file__)), url=url, method=method)

                try:
                    handle = open(path)
                    response.data = handle.read()
                    response.status = 200
                except IOError:
                    response.status = 404


class CanvasFileDownload_DAO(DAO):
    def service_name(self):
        return "canvas"

    def _get_live_implementation(self):
        return CanvasFileDownloadLiveDAO(self.service_name(), self)


class CanvasFileDownloadLiveDAO(LiveDAO):
    def _fix_url_host(self, url):
        # Ensure file url matches the hostname in settings,
        # to avoid mixing Canvas prod/test/beta hosts
        host = self.dao.get_service_setting("HOST")
        url = re.sub(r'^https://[^/]+', host, url)
        return url

    def load(self, method, url, headers, body):
        url = self._fix_url_host(url)
        pool = self.get_pool()
        return pool.urlopen(method, url, headers=headers)

    def get_pool(self):
        return self.create_pool()

    def create_pool(self):
        # Use a PoolManager to allow redirects to other hosts
        return PoolManager(
            cert_reqs="CERT_REQUIRED",
            ca_certs=self.dao.get_setting("CA_BUNDLE",
                                          "/etc/ssl/certs/ca-bundle.crt"),
            timeout=self._get_timeout(),
            maxsize=self._get_max_pool_size(),
            block=True,
            retries=Retry(total=1, connect=0, read=0, redirect=1))
