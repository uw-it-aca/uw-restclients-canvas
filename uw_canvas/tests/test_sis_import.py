# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


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

    def test_import_archive(self):
        canvas = SISImport()
        self.assertRaises(MissingAccountID, canvas.import_archive, None)


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
    def test_import_archive(self, mock_post):
        canvas = SISImport()
        canvas.import_archive('')
        mock_post.assert_called_with((
            '/api/v1/accounts/12345/sis_imports.json?'
            'import_type=instructure_csv'), {
                'Content-Type': 'application/zip'
            }, '')

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
        self.assertEqual(sis_import.import_id, 1)
        self.assertEqual(sis_import.workflow_state, "imported")
        self.assertEqual(sis_import.progress, "100")

    def _setup_sis_import(self):
        return SISImportModel(import_id=1)

    @mock.patch.object(SISImport, '_put_resource')
    def test_delete_import(self, mock_put):
        sis_import = SISImportModel(import_id=5)
        SISImport().delete_import(sis_import)
        mock_put.assert_called_with(
            '/api/v1/accounts/12345/sis_imports/5/abort')

    @mock.patch.object(SISImport, '_put_resource')
    def test_delete_all_pending_imports(self, mock_put):
        SISImport().delete_all_pending_imports()
        mock_put.assert_called_with(
            '/api/v1/accounts/12345/sis_imports/abort_all_pending')
