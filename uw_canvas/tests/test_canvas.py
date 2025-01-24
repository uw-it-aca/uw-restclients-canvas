# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas import Canvas, Canvas_DAO
import mock


@fdao_canvas_override
class CanvasTestCanvas(TestCase):
    def test_valid_canvas_id(self):
        canvas = Canvas()
        self.assertEqual(canvas.valid_canvas_id(11), True)
        self.assertEqual(canvas.valid_canvas_id(111111111111), True)
        self.assertEqual(canvas.valid_canvas_id(1), False)
        self.assertEqual(canvas.valid_canvas_id('ab'), False)
        self.assertEqual(canvas.valid_canvas_id('11111'), True)

    def test_sis_account_id(self):
        canvas = Canvas()
        self.assertEqual(canvas.sis_account_id('abc:def'),
                         'sis_account_id%3Aabc%3Adef')

    def test_sis_course_id(self):
        canvas = Canvas()
        self.assertEqual(canvas.sis_course_id('2013-spring-ESS-101-A'),
                         'sis_course_id%3A2013-spring-ESS-101-A')

    def test_sis_section_id(self):
        canvas = Canvas()
        self.assertEqual(canvas.sis_section_id('2013-spring-ESS-101-AB'),
                         'sis_section_id%3A2013-spring-ESS-101-AB')

    def test_sis_user_id(self):
        canvas = Canvas()
        self.assertEqual(
            canvas.sis_user_id('123456ABCDEF123456ABCDEF123456AB'),
            'sis_user_id%3A123456ABCDEF123456ABCDEF123456AB')

    def test_sis_login_id(self):
        canvas = Canvas()
        self.assertEqual(canvas.sis_login_id('javerage'),
                         'sis_login_id%3Ajaverage')

    def test_params(self):
        canvas = Canvas()

        self.assertEqual(canvas._params(None), '')
        self.assertEqual(canvas._params({}), '')

        params = {'per_page': 100}
        self.assertEqual(canvas._params(params), '?per_page=100')

        params = {'per_page': 100, 'terms': ['2013-autumn', '2014-winter']}
        self.assertEqual(
            canvas._params(params),
            '?per_page=100&terms[]=2013-autumn&terms[]=2014-winter')

        params = {'per_page': 100, 'search_term': '19th Century Poets'}
        self.assertEqual(
            canvas._params(params),
            '?per_page=100&search_term=19th%20Century%20Poets')

    @mock.patch.object(Canvas_DAO, '__init__')
    def test_api_host(self, mock_dao):
        mock_dao.return_value = None

        canvas = Canvas(canvas_api_host='canvas.test.edu')
        mock_dao.assert_called_with(canvas_api_host='canvas.test.edu')
