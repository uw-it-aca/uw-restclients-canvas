from unittest import TestCase
from uw_canvas.dao import CanvasFileDownload_DAO
from uw_canvas.utilities import ldao_canvas_override
from urllib3 import PoolManager
import mock


@ldao_canvas_override
class TestCanvasFileDownloadLiveDAO(TestCase):
    @mock.patch.object(PoolManager, 'urlopen')
    def test_file_download_dao(self, mock_pool):
        dao = CanvasFileDownload_DAO()
        r = dao.getURL('https://example.com/some/path')
        mock_pool.assert_called_with(
            'GET', 'https://canvas.test.edu/some/path', headers={})
