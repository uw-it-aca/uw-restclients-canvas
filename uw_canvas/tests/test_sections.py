from unittest import TestCase
from uw_canvas.utilities import fdao_canvas_override
from uw_canvas.sections import Sections


@fdao_canvas_override
class CanvasTestSections(TestCase):
    def test_sections(self):
        canvas = Sections()

        sections = canvas.get_sections_in_course_by_sis_id('2013-spring-CSE-142-A', {'include': ['students']})

        self.assertEquals(len(sections), 16, "Too few sections")

        n = 0
        for section in sections:
            n += len(section.students)

        self.assertEquals(n, 32, "Too few students")

    def test_sections_with_students(self):
        canvas = Sections()

        sections = canvas.get_sections_with_students_in_course_by_sis_id('2013-spring-CSE-142-A')

        self.assertEquals(len(sections), 16, "Too few sections")

        n = 0
        for section in sections:
            n += len(section.students)

        self.assertEquals(n, 32, "Too few students")
