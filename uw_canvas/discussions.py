# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0


from uw_canvas import Canvas
from uw_canvas.courses import COURSES_API
from uw_canvas.models import DiscussionTopic, DiscussionEntry

DISCUSSIONS_API = COURSES_API + "/discussion_topics"


class Discussions(Canvas):
    def get_discussion_topics_for_sis_course_id(self, sis_course_id, **params):
        url = DISCUSSIONS_API.format(self._sis_id(
            sis_course_id, sis_field="course"))
        data = self._get_paged_resource(url, params=params)

        topics = []

        for topic_data in data:
            topic = DiscussionTopic()
            topic.topic_id = topic_data["id"]
            topic.html_url = topic_data["url"]
            canvas_course_id = topic_data["url"].split("/")[-3]
            topic.course_id = canvas_course_id
            topics.append(topic)

        return topics

    def get_entries_for_topic(self, topic, **params):
        url = DISCUSSIONS_API.format(topic.course_id) + "/{}/entries".format(
            topic.topic_id)
        data = self._get_paged_resource(url, params=params)

        entries = []
        for entry_data in data:
            entry = DiscussionEntry()
            entry.entry_id = entry_data["id"]
            entry.user_id = entry_data["user_id"]
            entries.append(entry)

            replies_url = (
                DISCUSSIONS_API.format(topic.course_id) +
                "/{}/entries/{}/replies".format(topic.topic_id, entry.entry_id)
            )

            reply_data = self._get_paged_resource(replies_url)
            for reply_values in reply_data:
                entry = DiscussionEntry()
                entry.entry_id = reply_values["id"]
                entry.user_id = reply_values["user_id"]
                entries.append(entry)

        return entries
