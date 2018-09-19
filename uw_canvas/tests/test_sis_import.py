from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.sis_import import SISImport
from uw_canvas.models import SISImport as SISImportModel
from uw_canvas import MissingAccountID
import mock


class CanvasTestSISImportMissingAccount(TestCase):
    def test_import_str(self):
        canvas = SISImport()
        self.assertRaises(MissingAccountID, canvas.import_str, 'a,b,c,d,e,f')

    def test_import_dir(self):
        canvas = SISImport()
        self.assertRaises(MissingAccountID, canvas.import_dir, '/path/to/csv')


@fdao_canvas_override
class CanvasTestSISImport(TestCase):
    @mock.patch.object(SISImport, '_post_resource')
    def test_import_str(self, mock_post):
        canvas = SISImport()
        canvas.import_str('a,b,c,d,e,f')
        mock_post.assert_called_with((
            '/api/v1/accounts/12345/sis_imports.json?'
            'import_type=instructure_csv'), {
                'Content-Type': 'text/csv'
            }, 'a,b,c,d,e,f')

        # With extra params
        canvas.import_str('a,b,c,d,e,f',
                          params={'override_sis_stickiness': '1'})
        mock_post.assert_called_with((
            '/api/v1/accounts/12345/sis_imports.json?import_type='
            'instructure_csv&override_sis_stickiness=1'), {
                'Content-Type': 'text/csv'
            }, 'a,b,c,d,e,f')

    @mock.patch.object(SISImport, '_post_resource')
    @mock.patch.object(SISImport, '_build_archive')
    def test_import_dir(self, mock_build, mock_post):
        mock_build.return_value = ''
        canvas = SISImport()
        canvas.import_dir('/path/to/csv')
        mock_post.assert_called_with((
            '/api/v1/accounts/12345/sis_imports.json?'
            'import_type=instructure_csv'), {
                'Content-Type': 'application/zip'
            }, '')

    def test_get_import_status(self):
        canvas = SISImport()
        sis_import = canvas.get_import_status(self._setup_sis_import())
        self.assertEquals(sis_import.import_id, 1)
        self.assertEquals(sis_import.workflow_state, "imported")
        self.assertEquals(sis_import.progress, "100")

    def _setup_sis_import(self):
        return SISImportModel(import_id=1)
