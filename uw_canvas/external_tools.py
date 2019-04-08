from uw_canvas import Canvas
from uw_canvas.accounts import ACCOUNTS_API
from uw_canvas.courses import COURSES_API


class ExternalToolsException(Exception):
    pass


class ExternalTools(Canvas):
    def get_external_tools_in_account(self, account_id, params={}):
        """
        Return external tools for the passed canvas account id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = ACCOUNTS_API.format(account_id) + "/external_tools"

        external_tools = []
        for data in self._get_paged_resource(url, params=params):
            external_tools.append(data)
        return external_tools

    def get_external_tools_in_account_by_sis_id(self, sis_id):
        """
        Return external tools for given account sis id.
        """
        return self.get_external_tools_in_account(self._sis_id(sis_id,
                                                               "account"))

    def get_external_tools_in_course(self, course_id, params={}):
        """
        Return external tools for the passed canvas course id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = COURSES_API.format(course_id) + "/external_tools"

        external_tools = []
        for data in self._get_paged_resource(url, params=params):
            external_tools.append(data)
        return external_tools

    def get_external_tools_in_course_by_sis_id(self, sis_id):
        """
        Return external tools for given course sis id.
        """
        return self.get_external_tools_in_course(self._sis_id(sis_id,
                                                              "course"))

    def create_external_tool_in_course(self, course_id, json_data):
        return self._create_external_tool(COURSES_API, course_id, json_data)

    def create_external_tool_in_account(self, account_id, json_data):
        return self._create_external_tool(ACCOUNTS_API, account_id, json_data)

    def _create_external_tool(self, context, context_id, json_data):
        """
        Create an external tool using the passed json_data.

        context is either COURSES_API or ACCOUNTS_API.
        context_id is the Canvas course_id or account_id, depending on context.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create
        """
        url = context.format(context_id) + "/external_tools"
        return self._post_resource(url, body=json_data)

    def update_external_tool_in_course(self, course_id, external_tool_id,
                                       json_data):
        return self._update_external_tool(COURSES_API, course_id,
                                          external_tool_id, json_data)

    def update_external_tool_in_account(self, account_id, external_tool_id,
                                        json_data):
        return self._update_external_tool(ACCOUNTS_API, account_id,
                                          external_tool_id, json_data)

    def _update_external_tool(self, context, context_id, external_tool_id,
                              json_data):
        """
        Update the external tool identified by external_tool_id with the passed
        json data.

        context is either COURSES_API or ACCOUNTS_API.
        context_id is the course_id or account_id, depending on context

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.update
        """
        url = context.format(context_id) + "/external_tools/{}".format(
            external_tool_id)
        return self._put_resource(url, body=json_data)

    def delete_external_tool_in_course(self, course_id, external_tool_id):
        return self._delete_external_tool(COURSES_API, course_id,
                                          external_tool_id)

    def delete_external_tool_in_account(self, account_id, external_tool_id):
        return self._delete_external_tool(ACCOUNTS_API, account_id,
                                          external_tool_id)

    def _delete_external_tool(self, context, context_id, external_tool_id):
        """
        Delete the external tool identified by external_tool_id.

        context is either COURSES_API or ACCOUNTS_API.
        context_id is the course_id or account_id, depending on context

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.destroy
        """
        url = context.format(context_id) + "/external_tools/{}".format(
            external_tool_id)
        response = self._delete_resource(url)
        return True

    def _get_sessionless_launch_url(self, context, context_id, tool_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        url = context.format(context_id) + "/external_tools/sessionless_launch"
        params = {"id": tool_id}
        return self._get_resource(url, params)

    def get_sessionless_launch_url_from_account(self, tool_id, account_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self._get_sessionless_launch_url(
            ACCOUNTS_API, account_id, tool_id)

    def get_sessionless_launch_url_from_account_sis_id(
            self, tool_id, account_sis_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self.get_sessionless_launch_url_from_account(
            tool_id, self._sis_id(account_sis_id, "account"))

    def get_sessionless_launch_url_from_course(self, tool_id, course_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self._get_sessionless_launch_url(
            COURSES_API, course_id, tool_id)

    def get_sessionless_launch_url_from_course_sis_id(
            self, tool_id, course_sis_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self.get_sessionless_launch_url_from_course(
            tool_id, self._sis_id(course_sis_id, "course"))
