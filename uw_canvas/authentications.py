from uw_canvas import Canvas


class Authentications(Canvas):
    def get_authentication_count_for_sis_login_id_from_start_date(
            self, sis_login_id, start_date):
        url = "/api/v1/audit/authentication/users/sis_login_id:%s" % (
            sis_login_id)

        params = {
            'start_time': start_date
        }

        data = self._get_resource(url, params=params)

        return len(data["events"])
