from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.sections import Sections
from uw_canvas.models import CanvasSection
import mock


@fdao_canvas_override
class CanvasTestSections(TestCase):
    def test_sis_id(self):
        section = CanvasSection()
        self.assertEquals(section.sws_section_id(), None)
        self.assertEquals(section.sws_instructor_regid(), None)
        self.assertEquals(section.is_academic_sis_id(), False)

        section = CanvasSection(sis_section_id="2013-spring-PHYS-121-A--")
        self.assertEquals(section.sws_section_id(), "2013,spring,PHYS,121/A")
        self.assertEquals(section.sws_instructor_regid(), None)
        self.assertEquals(section.is_academic_sis_id(), True)

        section = CanvasSection(sis_section_id="2013-spring-PHYS-121-AB")
        self.assertEquals(section.sws_section_id(), "2013,spring,PHYS,121/AB")
        self.assertEquals(section.sws_instructor_regid(), None)
        self.assertEquals(section.is_academic_sis_id(), True)

        section = CanvasSection(
            sis_section_id=(
                "2013-spring-PHYS-599-A-9136CCB8F66711D5BE060004AC494FFE--"))
        self.assertEquals(section.sws_section_id(), "2013,spring,PHYS,599/A")
        self.assertEquals(
            section.sws_instructor_regid(), "9136CCB8F66711D5BE060004AC494FFE")
        self.assertEquals(section.is_academic_sis_id(), True)

        section = CanvasSection(sis_section_id="course_123456_groups")
        self.assertEquals(section.sws_section_id(), None)
        self.assertEquals(section.sws_instructor_regid(), None)
        self.assertEquals(section.is_academic_sis_id(), False)

    def test_sections(self):
        canvas = Sections()

        sections = canvas.get_sections_in_course_by_sis_id(
            '2013-spring-CSE-142-A', {'include': ['students']})

        self.assertEquals(len(sections), 16, "Too few sections")

        n = 0
        for section in sections:
            n += len(section.students)

        self.assertEquals(n, 32, "Too few students")

    def test_sections_with_students(self):
        canvas = Sections()

        sections = canvas.get_sections_with_students_in_course_by_sis_id(
            '2013-spring-CSE-142-A')

        self.assertEquals(len(sections), 16, "Too few sections")

        n = 0
        for section in sections:
            n += len(section.students)

        self.assertEquals(n, 32, "Too few students")

    @mock.patch.object(Sections, '_post_resource')
    def test_create_section(self, mock_create):
        mock_create.return_value = None
        canvas = Sections()

        canvas.create_section("123456", "Test Section", "test-section-id")
        mock_create.assert_called_with(
            '/api/v1/courses/123456/sections', {
                'course_section': {
                    'name': 'Test Section',
                    'sis_section_id': 'test-section-id'}})

    @mock.patch.object(Sections, '_put_resource')
    def test_update_section(self, mock_update):
        mock_update.return_value = None
        canvas = Sections()

        canvas.update_section("999999", "New Name", "test-section-id")
        mock_update.assert_called_with(
            '/api/v1/sections/999999', {
                'course_section': {
                    'name': 'New Name',
                    'sis_section_id': 'test-section-id'}})
