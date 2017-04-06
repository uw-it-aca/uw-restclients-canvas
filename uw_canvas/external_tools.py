from uw_canvas import Canvas


class ExternalToolsException(Exception):
    pass


class ExternalTools(Canvas):
    def get_external_tools_in_account(self, account_id, params={}):
        """
        Return external tools for the passed canvas account id.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.index
        """
        url = "/api/v1/accounts/%s/external_tools" % account_id

        external_tools = []
        for data in self._get_paged_resource(url, params=params):
            external_tools.append(self._external_tool_from_json(data))
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
        url = "/api/v1/courses/%s/external_tools" % course_id

        external_tools = []
        for data in self._get_paged_resource(url, params=params):
            external_tools.append(self._external_tool_from_json(data))
        return external_tools

    def get_external_tools_in_course_by_sis_id(self, sis_id):
        """
        Return external tools for given course sis id.
        """
        return self.get_external_tools_in_course(self._sis_id(sis_id,
                                                              "course"))

    def create_external_tool_in_course(self, course_id, json_data):
        return self._create_external_tool('courses', course_id, json_data)

    def create_external_tool_in_account(self, account_id, json_data):
        return self._create_external_tool('accounts', account_id, json_data)

    def _create_external_tool(self, context, context_id, json_data):
        """
        Create an external tool using the passed json_data.

        context is either 'courses' or 'accounts'.
        context_id is the Canvas course_id or account_id, depending on context.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.create
        """
        url = '/api/v1/%s/%s/external_tools' % (context, context_id)
        data = self._post_resource(url, body=json_data)
        return self._external_tool_from_json(data)

    def update_external_tool_in_course(self, course_id, external_tool_id,
                                       json_data):
        return self._update_external_tool('courses', course_id,
                                          external_tool_id, json_data)

    def update_external_tool_in_account(self, account_id, external_tool_id,
                                        json_data):
        return self._update_external_tool('accounts', account_id,
                                          external_tool_id, json_data)

    def _update_external_tool(self, context, context_id, external_tool_id,
                              json_data):
        """
        Update the external tool identified by external_tool_id with the passed
        json data.

        context is either 'courses' or 'accounts'.
        context_id is the course_id or account_id, depending on context

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.update
        """
        url = '/api/v1/%s/%s/external_tools/%s' % (context, context_id,
                                                   external_tool_id)
        data = self._put_resource(url, body=json_data)
        return self._external_tool_from_json(data)

    def delete_external_tool_in_course(self, course_id, external_tool_id):
        return self._delete_external_tool('courses', course_id,
                                          external_tool_id)

    def delete_external_tool_in_account(self, account_id, external_tool_id):
        return self._delete_external_tool('accounts', account_id,
                                          external_tool_id)

    def _delete_external_tool(self, context, context_id, external_tool_id):
        """
        Delete the external tool identified by external_tool_id.

        context is either 'courses' or 'accounts'.
        context_id is the course_id or account_id, depending on context

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.destroy
        """
        url = '/api/v1/%s/%s/external_tools/%s' % (context, context_id,
                                                   external_tool_id)
        response = self._delete_resource(url)
        return True

    def _external_tool_from_json(self, data):
        return data

    def _get_sessionless_launch_url(self, tool_id, context, context_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        url = "/api/v1/%ss/%s/external_tools/sessionless_launch" % (
            context, context_id)
        params = {
            "id": tool_id
        }

        return self._get_resource(url, params)

    def get_sessionless_launch_url_from_account(self, tool_id, account_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self._get_sessionless_launch_url(tool_id, "account", account_id)

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
        return self._get_sessionless_launch_url(tool_id, "course", course_id)

    def get_sessionless_launch_url_from_course_sis_id(
            self, tool_id, course_sis_id):
        """
        Get a sessionless launch url for an external tool.

        https://canvas.instructure.com/doc/api/external_tools.html#method.external_tools.generate_sessionless_launch
        """
        return self.get_sessionless_launch_url_from_course(
            tool_id, self._sis_id(course_sis_id, "course"))
