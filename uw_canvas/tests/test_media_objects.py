# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.media_objects import MediaObjects
from uw_canvas.models import MediaObject
import mock


@fdao_canvas_override
class CanvasTestMediaObjects(TestCase):
    def test_media_objects_by_course_id(self):
        canvas = MediaObjects()
        media_objects = canvas.get_media_objects_by_course_id('862539')
        self.assertEqual(len(media_objects), 1)

        media_object = media_objects[0]
        self.assertTrue(media_object.can_add_captions)
        self.assertEqual(media_object.user_entered_title, 'User Entered Title')
        self.assertEqual(media_object.title, 'Test Title')
        self.assertEqual(
            media_object.media_id, 'm-JYmy6TLsHkxcrhgYmqa7XW1HCH3wEYc')
        self.assertEqual(media_object.media_type, 'video')
        self.assertEqual(len(media_object.media_tracks), 2)
        self.assertEqual(len(media_object.media_sources), 2)

        media_track = media_object.media_tracks[1]
        self.assertEqual(media_track.kind, 'subtitles')
        self.assertEqual(
            media_track.created_at.isoformat(), '2012-09-27T20:29:17-06:00')
        self.assertEqual(
            media_track.updated_at.isoformat(), '2012-09-27T20:29:17-06:00')
        self.assertEqual(
            media_track.url,
            'https://canvas.uw.edu/media_objects/0_r949z9lk/media_tracks/14')
        self.assertEqual(media_track.id, 14)
        self.assertEqual(media_track.locale, 'cs')

        media_source = media_object.media_sources[1]
        self.assertEqual(media_source.height, '252')
        self.assertEqual(media_source.width, '336')
        self.assertEqual(media_source.content_type, 'video/x-flv')
        self.assertEqual(media_source.container_format, 'flash video')
        self.assertEqual(
            media_source.url,
            'http://example.com/p/100/sp/10000/download/entry_id/0_r949z9lk/'
            'flavor/0_0f2x4odx/ks/NmY2M2Q2MDdhMjBlMzA2ZmRhMWZjZjAxNWUyOTg0Mz'
            'A5MDI5NGE4ZXwxMDA7MTAwOzEzNDkyNzU5MDY7MDsxMzQ5MTg5NTA2LjI5MDM7O'
            '2Rvd25sb2FkOjBfcjk0OXo5bGs7/relocate/download.flv')
        self.assertEqual(media_source.bitrate, '797')
        self.assertEqual(media_source.size, '347')
        self.assertEqual(media_source.is_original, '1')
        self.assertEqual(media_source.file_ext, 'flv')

    def test_media_objects_by_course_sis_id(self):
        canvas = MediaObjects()
        media_objects = canvas.get_media_objects_by_course_sis_id(
            '2013-autumn-PHYS-248-A')
        self.assertEqual(len(media_objects), 1)
