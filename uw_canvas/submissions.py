from uw_canvas import Canvas
from uw_canvas.models import Submission, Attachment
import dateutil.parser


class Submissions(Canvas):
    def get_submissions_by_course_and_assignment(
            self, course_id, assignment_id, params={}):
        """
        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.index
        """
        url = '/api/v1/courses/%s/assignments/%s/submissions' % (
            course_id, assignment_id)

        submissions = []
        for data in self._get_paged_resource(url, params=params):
            submissions.append(self._submission_from_json(data))
        return submissions

    def get_submissions_multiple_assignments_by_sis_id(
            self, is_section, sis_id, students=None, assignments=None):
        """
        List submissions for multiple assignments by course/section sis id and
        optionally student

        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        if is_section:
            return self.get_submissions_multiple_assignments(
                is_section, self._sis_id(sis_id, 'section'), students,
                assignments)
        else:
            return self.get_submissions_multiple_assignments(
                is_section, self._sis_id(sis_id, 'course'), students,
                assignments)

    def get_submissions_multiple_assignments(
            self, is_section, course_id, students=None, assignments=None):
        """
        List submissions for multiple assignments by course/section id and
        optionally student

        https://canvas.instructure.com/doc/api/submissions.html#method.submissions_api.for_students
        """
        course_type = 'courses'
        if is_section:
            course_type = 'sections'
        params = {}
        if students is not None:
            params['student_ids'] = students
        if assignments is not None:
            params['assignments'] = assignments

        url = '/api/v1/%s/%s/students/submissions' % (course_type, course_id)
        data = self._get_paged_resource(url, params=params)
        submissions = []
        for submission in data:
            sub = self._submission_from_json(submission)
            submissions.append(sub)
        return submissions

    def _submission_from_json(self, data):
        submission = Submission()
        submission.submission_id = data['id']
        submission.body = data['body']
        submission.attempt = data['attempt']
        if data['submitted_at'] is not None:
            submitted_date_str = data['submitted_at']
            submission.submitted_at = dateutil.parser.parse(submitted_date_str)
        submission.assignment_id = data['assignment_id']
        submission.workflow_state = data['workflow_state']
        submission.preview_url = data['preview_url']
        submission.late = data['late']
        submission.grade = data['grade']
        submission.score = data['score']
        submission.grade_matches_current_submission = (
            data['grade_matches_current_submission'])
        submission.url = data['url']
        submission.grader_id = data['grader_id']
        if data['graded_at'] is not None:
            graded_date_str = data['graded_at']
            submission.graded_at = dateutil.parser.parse(graded_date_str)
        submission.submission_type = data['submission_type']

        submission.attachments = []
        for attachment_data in data.get('attachments', []):
            submission.attachments.append(Attachment(
                attachment_id=attachment_data['id'],
                filename=attachment_data['filename'],
                display_name=attachment_data['display_name'],
                content_type=attachment_data['content-type'],
                size=attachment_data['size'],
                url=attachment_data['url']))

        return submission
