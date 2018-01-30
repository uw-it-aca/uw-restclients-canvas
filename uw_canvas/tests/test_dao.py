from unittest import TestCase
from uw_canvas.dao import CanvasFileDownload_DAO
from commonconf import override_settings


@override_settings(RESTCLIENTS_CANVAS_HOST='https://canvas.test.edu')
class TestCanvasFileDownloadLiveDAO(TestCase):
    def test_fix_url_host(self):
        dao = CanvasFileDownload_DAO()._get_live_implementation()
        self.assertEquals(dao._fix_url_host('https://canvas.edu/some/path'),
                          'https://canvas.test.edu/some/path')

        self.assertEquals(dao._fix_url_host('https://canvas.test.edu/path'),
                          'https://canvas.test.edu/path')
