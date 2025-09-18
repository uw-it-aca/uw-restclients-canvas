# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.files import Files
from uw_canvas.models import File
import mock


@fdao_canvas_override
class CanvasTestFiles(TestCase):
    def test_get_course_files(self):
        client = Files()
        files = client.get_course_files("862539")

        self.assertEqual(len(files), 3)

        file = files[0]
        self.assertEqual(file.filename, "Exams.pdf")
        self.assertEqual(file.file_id, 14)
        self.assertEqual(file.size, 348600)
        self.assertEqual(file.content_type, "application/pdf")
