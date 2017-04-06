from uw_canvas import Canvas


class Conversations(Canvas):
    def get_conversation_ids_for_sis_login_id(self, sis_login_id):
        url = "/api/v1/conversations"

        params = {
            "as_user_id": self.sis_login_id(sis_login_id),
            "include_all_conversation_ids": "true"
        }

        data = self._get_resource(url, params=params)
        conversation_ids = []
        for conversation_id in data["conversation_ids"]:
            conversation_ids.append(conversation_id)

        return conversation_ids

    def get_data_for_conversation_id_as_sis_login_id(
            self, conversation_id, sis_login_id):
        url = "/api/v1/conversations/%s" % (conversation_id)
        params = {
            "as_user_id": self.sis_login_id(sis_login_id)
        }

        return self._get_resource(url, params=params)
