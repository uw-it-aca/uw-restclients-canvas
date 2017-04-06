from uw_canvas import Canvas
from uw_canvas.models import GradingStandard


class GradingStandards(Canvas):
    def get_grading_standards_for_course(self, course_id):
        """
        List the grading standards available to a course
        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.context_index
        """
        url = "/api/v1/courses/%s/grading_standards" % course_id

        standards = []
        for data in self._get_resource(url):
            standards.append(self._grading_standard_from_json(data))
        return standards

    def create_grading_standard_for_course(self, course_id, name,
                                           grading_scheme, creator):
        """
        Create a new grading standard for the passed course.

        https://canvas.instructure.com/doc/api/grading_standards.html#method.grading_standards_api.create
        """
        url = "/api/v1/courses/%s/grading_standards" % course_id
        body = {
            "title": name,
            "grading_scheme_entry": grading_scheme,
            "as_user_id": creator
        }

        data = self._post_resource(url, body)

        return self._grading_standard_from_json(data)

    def _grading_standard_from_json(self, data):
        grading_standard = GradingStandard()
        grading_standard.grading_standard_id = data["id"]
        grading_standard.title = data["title"]
        grading_standard.context_type = data["context_type"]
        grading_standard.context_id = data["context_id"]
        grading_standard.grading_scheme = data["grading_scheme"]
        return grading_standard
