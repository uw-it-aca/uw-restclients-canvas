# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import CanvasSection

SECTIONS_API = "/api/v1/sections/{}"


class Sections(Canvas):
    def get_section(self, section_id, params={}):
        """
        Return section resource for given canvas section id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.show
        """
        url = SECTIONS_API.format(section_id)
        return CanvasSection(data=self._get_resource(url, params=params))

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
        url = COURSES_API.format(course_id) + "/sections"

        sections = []
        for data in self._get_paged_resource(url, params=params):
            sections.append(CanvasSection(data=data))

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
        url = COURSES_API.format(course_id) + "/sections"
        body = {"course_section": {"name": name,
                                   "sis_section_id": sis_section_id}}

        return CanvasSection(data=self._post_resource(url, body))

    def update_section(self, section_id, name, sis_section_id):
        """
        Update a canvas section with the given section id.

        https://canvas.instructure.com/doc/api/sections.html#method.sections.update
        """
        url = SECTIONS_API.format(section_id)
        body = {"course_section": {}}

        if name:
            body["course_section"]["name"] = name

        if sis_section_id:
            body["course_section"]["sis_section_id"] = sis_section_id

        return CanvasSection(data=self._put_resource(url, body))
