from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import GradingStandard


class GradingStandards(Canvas):
    def get_grading_standards_for_course(self, course_id):
        """
        List the grading standards available to a course
        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        url = COURSES_API.format(course_id) + "/grading_standards"

        standards = []
        for data in self._get_resource(url):
            standards.append(GradingStandard(data=data))
        return standards

    def create_grading_standard_for_course(self, course_id, name,
                                           grading_scheme, creator):
        """
        Create a new grading standard for the passed course.

        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create
        """
        url = COURSES_API.format(course_id) + "/grading_standards"
        body = {
            "title": name,
            "grading_scheme_entry": grading_scheme,
            "as_user_id": creator
        }

        return GradingStandard(data=self._post_resource(url, body))
