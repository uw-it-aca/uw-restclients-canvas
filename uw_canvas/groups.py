from uw_canvas import Canvas


class Groups(Canvas):
    def get_groups_for_sis_course_id(self, sis_course_id):
        url = "/api/v1/courses/%s/groups" % self._sis_id(
            sis_course_id, sis_field="course")
        data = self._get_resource(url)

        raise Exception("Not implemented")
