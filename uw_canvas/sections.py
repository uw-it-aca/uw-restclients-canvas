from uw_canvas import Canvas
from uw_canvas.users import Users
from uw_canvas.models import CanvasSection


class Sections(Canvas):
    def get_section(self, section_id, params={}):
        """
        Return section resource for given canvas section id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.show
        """
        url = "/api/v1/sections/%s" % (section_id)
        return self._section_from_json(self._get_resource(url, params=params))

    def get_section_by_sis_id(self, sis_section_id, params={}):
        """
        Return section resource for given sis id.
        """
        return self.get_section(
            self._sis_id(sis_section_id, sis_field="section"), params)

    def get_sections_in_course(self, course_id, params={}):
        """
        Return list of sections for the passed course ID.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.index
        """
        url = "/api/v1/courses/%s/sections" % (course_id)

        sections = []
        for data in self._get_paged_resource(url, params=params):
            sections.append(self._section_from_json(data))

        return sections

    def get_sections_in_course_by_sis_id(self, sis_course_id, params={}):
        """
        Return list of sections for the passed course SIS ID.
        """
        return self.get_sections_in_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def get_sections_with_students_in_course(self, course_id, params={}):
        """
        Return list of sections including students for the passed course ID.
        """
        include = params.get("include", [])
        if "students" not in include:
            include.append("students")
        params["include"] = include

        return self.get_sections_in_course(course_id, params)

    def get_sections_with_students_in_course_by_sis_id(self, sis_course_id,
                                                       params={}):
        """
        Return list of sections including students for the passed sis ID.
        """
        return self.get_sections_with_students_in_course(
            self._sis_id(sis_course_id, sis_field="course"), params)

    def create_section(self, course_id, name, sis_section_id):
        """
        Create a canvas section in the given course id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.create
        """
        url = "/api/v1/courses/%s/sections" % course_id
        body = {"course_section": {"name": name,
                                   "sis_section_id": sis_section_id}}

        data = self._post_resource(url, body)
        return self._section_from_json(data)

    def update_section(self, section_id, name, sis_section_id):
        """
        Update a canvas section with the given section id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.update
        """
        url = "/api/v1/sections/%s" % section_id
        body = {"course_section": {}}

        if name:
            body["course_section"]["name"] = name

        if sis_section_id:
            body["course_section"]["sis_section_id"] = sis_section_id

        data = self._put_resource(url, body)
        return self._section_from_json(data)

    def _section_from_json(self, data):
        section = CanvasSection()
        section.section_id = data["id"]
        section.sis_section_id = data.get("sis_section_id", None)
        section.name = data["name"]
        section.course_id = data["course_id"]
        section.nonxlist_course_id = data.get("nonxlist_course_id", None)

        if "students" in data:
            users = Users()
            section.students = []
            for student_data in data["students"]:
                user = users._user_from_json(student_data)
                section.students.append(user)

        return section
