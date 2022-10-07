# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas import Canvas


@fdao_canvas_override
class CanvasTestCanvas(TestCase):
    def test_valid_canvas_id(self):
        canvas = Canvas()
        self.assertEquals(canvas.valid_canvas_id(11), True)
        self.assertEquals(canvas.valid_canvas_id(111111111111), True)
        self.assertEquals(canvas.valid_canvas_id(1), False)
        self.assertEquals(canvas.valid_canvas_id('ab'), False)
        self.assertEquals(canvas.valid_canvas_id('11111'), True)

    def test_sis_account_id(self):
        canvas = Canvas()
        self.assertEquals(canvas.sis_account_id('abc:def'),
                          'sis_account_id%3Aabc%3Adef')

    def test_sis_course_id(self):
        canvas = Canvas()
        self.assertEquals(canvas.sis_course_id('2013-spring-ESS-101-A'),
                          'sis_course_id%3A2013-spring-ESS-101-A')

    def test_sis_section_id(self):
        canvas = Canvas()
        self.assertEquals(canvas.sis_section_id('2013-spring-ESS-101-AB'),
                          'sis_section_id%3A2013-spring-ESS-101-AB')

    def test_sis_user_id(self):
        canvas = Canvas()
        self.assertEquals(
            canvas.sis_user_id('123456ABCDEF123456ABCDEF123456AB'),
            'sis_user_id%3A123456ABCDEF123456ABCDEF123456AB')

    def test_sis_login_id(self):
        canvas = Canvas()
        self.assertEquals(canvas.sis_login_id('javerage'),
                          'sis_login_id%3Ajaverage')

    def test_params(self):
        canvas = Canvas()

        self.assertEquals(canvas._params(None), '')
        self.assertEquals(canvas._params({}), '')

        params = {'per_page': 100}
        self.assertEquals(canvas._params(params), '?per_page=100')

        params = {'per_page': 100, 'terms': ['2013-autumn', '2014-winter']}
        self.assertEquals(
            canvas._params(params),
            '?per_page=100&terms[]=2013-autumn&terms[]=2014-winter')

        params = {'per_page': 100, 'search_term': '19th Century Poets'}
        self.assertEquals(
            canvas._params(params),
            '?per_page=100&search_term=19th%20Century%20Poets')
