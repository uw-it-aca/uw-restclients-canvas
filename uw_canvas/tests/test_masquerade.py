# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from restclients_core.exceptions import DataFailureException
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas import Canvas


@fdao_canvas_override
class CanvasMasquerade(TestCase):
    def test_no_masquerade(self):
        canvas = Canvas()
        self.assertEquals(canvas._as_user, None)

        params = {}
        canvas._set_as_user(params)
        self.assertEquals(len(params), 0)

    def test_has_masquerade(self, user='ABCDEF'):
        canvas = Canvas(as_user=user)
        self.assertEquals(canvas._as_user, user)

        params = {}
        canvas._set_as_user(params)
        self.assertEquals(params, {'as_user_id': 'sis_user_id:%s' % user})

    def test_masquerade_get(self):
        canvas = Canvas(as_user='ABCDEF')
        try:
            r = canvas._get_resource('/fake_api')
        except DataFailureException as ex:
            self.assertEquals(
                ex.url, '/fake_api?as_user_id=sis_user_id%3AABCDEF')

    def test_masquerade_put(self):
        canvas = Canvas(as_user='ABCDEF')
        try:
            r = canvas._put_resource('/fake_api', None)
        except DataFailureException as ex:
            self.assertEquals(
                ex.url, '/fake_api?as_user_id=sis_user_id%3AABCDEF')

    def test_masquerade_post(self):
        canvas = Canvas(as_user='ABCDEF')
        try:
            r = canvas._post_resource('/fake_api', None)
        except DataFailureException as ex:
            self.assertEquals(
                ex.url, '/fake_api?as_user_id=sis_user_id%3AABCDEF')

    def test_masquerade_delete(self):
        canvas = Canvas(as_user='ABCDEF')
        try:
            r = canvas._delete_resource('/fake_api')
        except DataFailureException as ex:
            self.assertEquals(
                ex.url, '/fake_api?as_user_id=sis_user_id%3AABCDEF')
