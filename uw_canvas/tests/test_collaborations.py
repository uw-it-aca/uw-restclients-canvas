# Copyright 2024 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.collaborations import Collaborations
from uw_canvas.models import Collaboration
import mock


@fdao_canvas_override
class CanvasTestCollaborations(TestCase):
    def test_get_collaborations_for_course(self):
        canvas = Collaborations()
        collaborations = canvas.get_collaborations_for_course("862539")
        collaboration = collaborations[0]
        self.assertEqual(collaboration.collaboration_id, 67)
        self.assertEqual(collaboration.collaboration_type, "Microsoft Office")
        self.assertEqual(collaboration.document_id,
                         "111111111111111111111111111")
        self.assertEqual(collaboration.user_id, 92)
        self.assertEqual(collaboration.context_id, 862539)
        self.assertEqual(collaboration.context_type, "Course")
        self.assertEqual(collaboration.url, None)
        self.assertEqual(str(collaboration.created_at),
                         "2012-06-01 00:00:00-06:00")
        self.assertEqual(str(collaboration.updated_at),
                         "2012-06-01 00:00:00-06:00")
        self.assertEqual(collaboration.description, None)
        self.assertEqual(collaboration.title, None)
