from restclients_core import models


class CanvasAccount(models.Model):
    account_id = models.IntegerField()
    sis_account_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=500)
    parent_account_id = models.CharField(max_length=30)
    root_account_id = models.CharField(max_length=30)


class CanvasSSOSettings(models.Model):
    login_handle_name = models.CharField(max_length=100, null=True)
    change_password_url = models.CharField(max_length=500, null=True)
    auth_discovery_url = models.CharField(max_length=500, null=True)
    unknown_user_url = models.CharField(max_length=500, null=True)

    def json_data(self):
        return {'sso_settings': {
            'login_handle_name': self.login_handle_name,
            'change_password_url': self.change_password_url,
            'auth_discovery_url': self.auth_discovery_url,
            'unknown_user_url': self.unknown_user_url
        }}


class CanvasRole(models.Model):
    role_id = models.IntegerField()
    label = models.CharField(max_length=200)
    base_role_type = models.CharField(max_length=200)
    workflow_state = models.CharField(max_length=50)


class CanvasTerm(models.Model):
    term_id = models.IntegerField()
    sis_term_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    workflow_state = models.CharField(max_length=50)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)


class CanvasCourse(models.Model):
    course_id = models.IntegerField()
    sis_course_id = models.CharField(max_length=100, null=True)
    account_id = models.IntegerField()
    term = models.ForeignKey(CanvasTerm, null=True)
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    course_url = models.CharField(max_length=2000)
    workflow_state = models.CharField(max_length=50)
    public_syllabus = models.NullBooleanField()
    syllabus_body = models.TextField(null=True)

    def is_unpublished(self):
        return self.workflow_state.lower() == "unpublished"

    def sws_course_id(self):
        if self.sis_course_id is None:
            return None

        parts = self.sis_course_id.split("-")
        if len(parts) != 5:
            return None

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                     parts[4])

        return sws_id


class CanvasSection(models.Model):
    section_id = models.IntegerField()
    sis_section_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200)
    course_id = models.IntegerField()
    nonxlist_course_id = models.IntegerField()


class CanvasEnrollment(models.Model):
    STUDENT = "StudentEnrollment"
    TEACHER = "TeacherEnrollment"
    TA = "TaEnrollment"
    OBSERVER = "ObserverEnrollment"
    DESIGNER = "DesignerEnrollment"

    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (TEACHER, "Teacher"),
        (TA, "TA"),
        (OBSERVER, "Observer"),
        (DESIGNER, "Designer")
    )

    STATUS_ACTIVE = "active"
    STATUS_INVITED = "invited"
    STATUS_PENDING = "creation_pending"
    STATUS_DELETED = "deleted"
    STATUS_REJECTED = "rejected"
    STATUS_COMPLETED = "completed"
    STATUS_INACTIVE = "inactive"

    STATUS_CHOICES = (
        (STATUS_ACTIVE, STATUS_ACTIVE),
        (STATUS_INVITED, STATUS_INVITED),
        (STATUS_PENDING, STATUS_PENDING),
        (STATUS_DELETED, STATUS_DELETED),
        (STATUS_REJECTED, STATUS_REJECTED),
        (STATUS_COMPLETED, STATUS_COMPLETED),
        (STATUS_INACTIVE, STATUS_INACTIVE)
    )

    user_id = models.IntegerField()
    course_id = models.IntegerField()
    section_id = models.IntegerField()
    login_id = models.CharField(max_length=80, null=True)
    sis_user_id = models.CharField(max_length=32, null=True)
    role = models.CharField(max_length=80, choices=ROLE_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    name = models.CharField(max_length=100)
    sortable_name = models.CharField(max_length=100)
    html_url = models.CharField(max_length=1000)
    sis_section_id = models.CharField(max_length=100, null=True)
    sis_course_id = models.CharField(max_length=100, null=True)
    course_url = models.CharField(max_length=2000, null=True)
    course_name = models.CharField(max_length=100, null=True)
    current_score = models.DecimalField(max_digits=10,
                                        decimal_places=2, null=True)
    final_score = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=True)
    current_grade = models.TextField(max_length=12, null=True)
    final_grade = models.TextField(max_length=12, null=True)
    grade_html_url = models.CharField(max_length=1000)
    total_activity_time = models.IntegerField(null=True)
    last_activity_at = models.DateTimeField(null=True)
    limit_privileges_to_course_section = models.NullBooleanField()

    def sws_course_id(self):
        if self.sis_course_id is None:
            return None

        parts = self.sis_course_id.split("-")

        if len(parts) != 5:
            return None

        sws_id = "%s,%s,%s,%s/%s" % (parts[0], parts[1], parts[2], parts[3],
                                     parts[4])

        return sws_id

    def json_data(self):
        return {"user_id": self.user_id,
                "course_id": self.course_id,
                "section_id": self.section_id,
                "login_id": self.login_id,
                "sis_user_id": self.sis_user_id,
                "role": self.role,
                "status": self.status,
                "current_score": self.current_score,
                "final_score": self.final_score,
                "current_grade": self.current_grade,
                "final_grade": self.final_grade}


class Attachment(models.Model):
    attachment_id = models.IntegerField()
    filename = models.CharField(max_length=100)
    display_name = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50)
    size = models.IntegerField()
    url = models.CharField(max_length=500)


class Report(models.Model):
    report_id = models.IntegerField()
    account_id = models.IntegerField()
    type = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    progress = models.SmallIntegerField(max_length=3, default=0)
    attachment = models.ForeignKey(Attachment, null=True)


class ReportType(models.Model):
    PROVISIONING = "provisioning_csv"
    SIS_EXPORT = "sis_export_csv"
    UNUSED_COURSES = "unused_courses_csv"

    NAME_CHOICES = (
        (PROVISIONING, "Provisioning"),
        (SIS_EXPORT, "SIS Export"),
        (UNUSED_COURSES, "Unused Courses")
    )

    name = models.CharField(max_length=500, choices=NAME_CHOICES)
    title = models.CharField(max_length=500)


class SISImport(models.Model):
    CSV_IMPORT_TYPE = "instructure_csv"

    import_id = models.IntegerField()
    workflow_state = models.CharField(max_length=100)
    progress = models.CharField(max_length=3)


class CanvasUser(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=100, null=True)
    short_name = models.CharField(max_length=100, null=True)
    sortable_name = models.CharField(max_length=100, null=True)
    sis_user_id = models.CharField(max_length=100, null=True)
    login_id = models.CharField(max_length=100, null=True)
    time_zone = models.CharField(max_length=100, null=True)
    locale = models.CharField(max_length=2, null=True)
    email = models.CharField(max_length=100, null=True)
    avatar_url = models.CharField(max_length=500, null=True)

    def post_data(self):
        return {"user": {"name": self.name,
                         "short_name": self.short_name,
                         "sortable_name": self.sortable_name,
                         "time_zone": self.time_zone,
                         "locale": self.locale},
                "pseudonym": {"unique_id": self.login_id,
                              "sis_user_id": self.sis_user_id,
                              "send_confirmation": False},
                "communication_channel": {"type": "email",
                                          "address": self.email,
                                          "skip_confirmation": True}}


class Login(models.Model):
    login_id = models.IntegerField()
    account_id = models.IntegerField()
    sis_user_id = models.CharField(max_length=100, null=True)
    unique_id = models.CharField(max_length=100, null=True)
    user_id = models.IntegerField()

    def put_data(self):
        return {"login": {"unique_id": self.unique_id,
                          "sis_user_id": self.sis_user_id}}


class CanvasAdmin(models.Model):
    admin_id = models.IntegerField()
    role = models.CharField(max_length=100)
    user = models.ForeignKey(CanvasUser)


class Submission(models.Model):
    submission_id = models.IntegerField()
    body = models.TextField(null=True)
    attempt = models.IntegerField(max_length=2)
    submitted_at = models.DateTimeField()
    assignment_id = models.IntegerField()
    workflow_state = models.CharField(max_length=100, null=True)
    preview_url = models.CharField(max_length=500)
    late = models.NullBooleanField()
    grade = models.TextField(max_length=12, null=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    grade_matches_current_submission = models.NullBooleanField()
    url = models.CharField(max_length=500, null=True)
    grader_id = models.IntegerField()
    graded_at = models.DateTimeField(null=True)
    submission_type = models.CharField(max_length=100, null=True)


class Assignment(models.Model):
    assignment_id = models.IntegerField()
    course_id = models.IntegerField()
    integration_id = models.CharField(max_length=200)
    integration_data = models.CharField(max_length=1500)
    due_at = models.DateTimeField(null=True)
    points_possible = models.IntegerField()
    grading_type = models.CharField(max_length=20)
    grading_standard_id = models.IntegerField(null=True)
    position = models.IntegerField()
    name = models.CharField(max_length=500)
    muted = models.NullBooleanField()
    html_url = models.CharField(max_length=500, null=True)

    def json_data(self):
        return {"assignment": {
                "integration_id": self.integration_id,
                "integration_data": self.integration_data}}


class Quiz(models.Model):
    quiz_id = models.IntegerField()
    due_at = models.DateTimeField()
    title = models.CharField(max_length=500)
    html_url = models.CharField(max_length=500, null=True)
    published = models.NullBooleanField()


class GradingStandard(models.Model):
    COURSE_CONTEXT = "Course"
    ACCOUNT_CONTEXT = "Account"

    CONTEXT_CHOICES = (
        (COURSE_CONTEXT, COURSE_CONTEXT),
        (ACCOUNT_CONTEXT, ACCOUNT_CONTEXT)
    )

    grading_standard_id = models.IntegerField()
    title = models.CharField(max_length=500)
    context_id = models.IntegerField()
    context_type = models.CharField(max_length=20, choices=CONTEXT_CHOICES)
    grading_scheme = models.TextField()


class DiscussionTopic(models.Model):
    topic_id = models.IntegerField()
    html_url = models.CharField(max_length=500, null=True)
    course_id = models.IntegerField()


class DiscussionEntry(models.Model):
    entry_id = models.IntegerField()
    user_id = models.IntegerField()
