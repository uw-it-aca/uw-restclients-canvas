# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.dao import CanvasFileDownload_DAO
from commonconf import override_settings


@override_settings(RESTCLIENTS_CANVAS_HOST='https://canvas.test.edu',
                   RESTCLIENTS_CANVAS_TIMEOUT='60',
                   RESTCLIENTS_CANVAS_POOL_SIZE='10')
class TestCanvasFileDownloadLiveDAO(TestCase):
    def test_fix_url_host(self):
        dao = CanvasFileDownload_DAO()._get_live_implementation()
        self.assertEquals(dao._fix_url_host('https://canvas.edu/some/path'),
                          'https://canvas.test.edu/some/path')

        self.assertEquals(dao._fix_url_host('https://canvas.test.edu/path'),
                          'https://canvas.test.edu/path')

    def test_get_settings(self):
        dao = CanvasFileDownload_DAO()._get_live_implementation()
        self.assertEquals(dao._get_timeout(), 60)
        self.assertEquals(dao._get_max_pool_size(), 10)
