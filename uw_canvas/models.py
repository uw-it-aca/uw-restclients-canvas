from restclients_core import models
import dateutil.parser
import re


class CanvasAccount(models.Model):
    account_id = models.IntegerField()
    sis_account_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=500)
    parent_account_id = models.CharField(max_length=30)
    root_account_id = models.CharField(max_length=30)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(CanvasAccount, self).__init__(*args, **kwargs)

        self.account_id = data["id"]
        self.sis_account_id = data.get("sis_account_id")
        self.name = data["name"]
        self.parent_account_id = data["parent_account_id"]
        self.root_account_id = data["root_account_id"]


class CanvasSSOSettings(models.Model):
    login_handle_name = models.CharField(max_length=100, null=True)
    change_password_url = models.CharField(max_length=500, null=True)
    auth_discovery_url = models.CharField(max_length=500, null=True)
    unknown_user_url = models.CharField(max_length=500, null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(CanvasSSOSettings, self).__init__(*args, **kwargs)

        sso_data = data['sso_settings']
        self.change_password_url = sso_data['change_password_url']
        self.login_handle_name = sso_data['login_handle_name']
        self.unknown_user_url = sso_data['unknown_user_url']
        self.auth_discovery_url = sso_data['auth_discovery_url']

    def json_data(self):
        return {
            'login_handle_name': self.login_handle_name,
            'change_password_url': self.change_password_url,
            'auth_discovery_url': self.auth_discovery_url,
            'unknown_user_url': self.unknown_user_url
        }


class CanvasRole(models.Model):
    role_id = models.IntegerField()
    label = models.CharField(max_length=200)
    base_role_type = models.CharField(max_length=200)
    workflow_state = models.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        self.permissions = {}

        data = kwargs.get("data")
        if data is None:
            return super(CanvasRole, self).__init__(*args, **kwargs)

        self.role_id = data["id"]
        self.label = data["label"]
        self.base_role_type = data["base_role_type"]
        self.workflow_state = data["workflow_state"]
        self.permissions = data.get("permissions", {})
        if "account" in data:
            self.account = CanvasAccount(data=data["account"])

    def json_data(self):
        return {
            "id": self.role_id,
            "label": self.label,
            "base_role_type": self.base_role_type,
            "workflow_state": self.workflow_state,
            "permissions": self.permissions,
        }


class CanvasTerm(models.Model):
    term_id = models.IntegerField()
    sis_term_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    workflow_state = models.CharField(max_length=50)
    start_at = models.DateTimeField(null=True)
    end_at = models.DateTimeField(null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(CanvasTerm, self).__init__(*args, **kwargs)

        self.term_id = data.get('id')
        self.sis_term_id = data.get('sis_term_id')
        self.name = data.get('name')
        self.workflow_state = data.get('workflow_state')
        if 'start_at' in data and data['start_at']:
            self.start_at = dateutil.parser.parse(data['start_at'])
        if 'end_at' in data and data['end_at']:
            self.end_at = dateutil.parser.parse(data['end_at'])
        self.overrides = data.get('overrides', {})


class CanvasCourse(models.Model):
    RE_COURSE_SIS_ID = re.compile(
        r"^\d{4}-"                           # year
        r"(?:winter|spring|summer|autumn)-"  # quarter
        r"[\w& ]+-"                          # curriculum
        r"\d{3}-"                            # course number
        r"[A-Z][A-Z0-9]?"                    # section id
        r"(?:-[A-F0-9]{32})?$",              # ind. study instructor regid
        re.VERBOSE)

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

    def __init__(self, *args, **kwargs):
        self.students = []

        data = kwargs.get("data")
        if data is None:
            return super(CanvasCourse, self).__init__(*args, **kwargs)

        self.course_id = data["id"]
        self.sis_course_id = data.get("sis_course_id")
        self.account_id = data["account_id"]
        self.code = data["course_code"]
        self.name = data["name"]
        self.workflow_state = data["workflow_state"]
        self.public_syllabus = data["public_syllabus"]

        course_url = data["calendar"]["ics"]
        course_url = re.sub(r"(.*?[a-z]/).*", r"\1", course_url)
        self.course_url = "{}courses/{}".format(course_url, data["id"])

        if "term" in data:
            self.term = CanvasTerm(data=data["term"])

        if "syllabus_body" in data:
            self.syllabus_body = data["syllabus_body"]

    def is_unpublished(self):
        return self.workflow_state.lower() == "unpublished"

    def sws_course_id(self):
        if not self.is_academic_sis_id():
            return

        try:
            (year, quarter, curr_abbr, course_num,
                section_id, reg_id) = self.sis_course_id.split('-', 5)
        except ValueError:
            (year, quarter, curr_abbr, course_num,
                section_id) = self.sis_course_id.split('-', 4)

        return '%s,%s,%s,%s/%s' % (
            year, quarter.lower(), curr_abbr.upper(), course_num, section_id)

    def sws_instructor_regid(self):
        if not self.is_academic_sis_id():
            return

        try:
            (year, quarter, curr_abbr, course_num,
                section_id, reg_id) = self.sis_course_id.split('-', 5)
        except ValueError:
            reg_id = None

        return reg_id

    def is_academic_sis_id(self):
        if (self.sis_course_id is None or
                self.RE_COURSE_SIS_ID.match(self.sis_course_id) is None):
            return False
        return True


class CanvasSection(models.Model):
    RE_SECTION_SIS_ID = re.compile(
        r"^\d{4}-"                                  # year
        r"(?:winter|spring|summer|autumn)-"         # quarter
        r"[\w& ]+-"                                 # curriculum
        r"\d{3}-"                                   # course number
        r"[A-Z](?:[A-Z0-9]|--|-[A-F0-9]{32}--)?$",  # section id|regid
        re.VERBOSE)

    section_id = models.IntegerField()
    sis_section_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=200)
    course_id = models.IntegerField()
    nonxlist_course_id = models.IntegerField()

    def __init__(self, *args, **kwargs):
        self.students = []

        data = kwargs.get("data")
        if data is None:
            return super(CanvasSection, self).__init__(*args, **kwargs)

        self.section_id = data["id"]
        self.sis_section_id = data.get("sis_section_id")
        self.name = data["name"]
        self.course_id = data["course_id"]
        self.nonxlist_course_id = data.get("nonxlist_course_id")

        for student_data in data.get("students", []):
            self.students.append(CanvasUser(data=student_data))

    def sws_section_id(self):
        if not self.is_academic_sis_id():
            return

        sis_section_id = re.sub(r'--$', '', self.sis_section_id)
        try:
            (year, quarter, curr_abbr, course_num,
                section_id, reg_id) = sis_section_id.split('-', 5)
        except ValueError:
            (year, quarter, curr_abbr, course_num,
                section_id) = sis_section_id.split('-', 4)

        return '%s,%s,%s,%s/%s' % (
            year, quarter.lower(), curr_abbr.upper(), course_num, section_id)

    def sws_instructor_regid(self):
        if not self.is_academic_sis_id():
            return

        section_id = re.sub(r'--$', '', self.sis_section_id)
        try:
            (year, quarter, curr_abbr, course_num,
                section_id, reg_id) = section_id.split('-', 5)
        except ValueError:
            reg_id = None

        return reg_id

    def is_academic_sis_id(self):
        if (self.sis_section_id is None or
                self.RE_SECTION_SIS_ID.match(self.sis_section_id) is None):
            return False
        return True


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

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(CanvasEnrollment, self).__init__(*args, **kwargs)

        self.user_id = data["user_id"]
        self.course_id = data["course_id"]
        self.section_id = data["course_section_id"]
        self.sis_course_id = data.get("sis_course_id", None)
        self.sis_section_id = data.get("sis_section_id", None)
        self.role = data["type"]
        self.status = data["enrollment_state"]
        self.html_url = data["html_url"]
        self.total_activity_time = data["total_activity_time"]
        self.limit_privileges_to_course_section = data.get(
            "limit_privileges_to_course_section", False)
        if data["last_activity_at"] is not None:
            self.last_activity_at = dateutil.parser.parse(
                data["last_activity_at"])

        if "user" in data:
            user_data = data["user"]
            self.name = user_data.get("name", None)
            self.sortable_name = user_data.get("sortable_name", None)
            self.login_id = user_data.get("login_id", None)
            self.sis_user_id = user_data.get("sis_user_id", None)

        if "grades" in data:
            grade_data = data["grades"]
            self.current_score = grade_data.get("current_score", None)
            self.final_score = grade_data.get("final_score", None)
            self.current_grade = grade_data.get("current_grade", None)
            self.final_grade = grade_data.get("final_grade", None)
            self.grade_html_url = grade_data.get("html_url", None)

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

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(Attachment, self).__init__(*args, **kwargs)

        self.attachment_id = data["id"]
        self.filename = data["filename"]
        self.display_name = data["display_name"]
        self.content_type = data["content-type"]
        self.size = data["size"]
        self.url = data["url"]


class Report(models.Model):
    report_id = models.IntegerField()
    account_id = models.IntegerField()
    type = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    status = models.CharField(max_length=50)
    progress = models.SmallIntegerField(max_length=3, default=0)
    attachment = models.ForeignKey(Attachment, null=True)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(Report, self).__init__(*args, **kwargs)

        self.account_id = data["account_id"]
        self.report_id = data["id"]
        self.type = data["report"]
        self.url = data["file_url"]
        self.status = data["status"]
        self.progress = data["progress"]
        self.parameters = data["parameters"]

        if "attachment" in data:
            self.attachment = Attachment(data=data["attachment"])


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

    def __init__(self, *args, **kwargs):
        self.parameters = {}
        self.last_run = None

        data = kwargs.get("data")
        if data is None:
            return super(ReportType, self).__init__(*args, **kwargs)

        self.name = data["report"]
        self.title = data["title"]
        self.parameters = data["parameters"]
        if "last_run" in data and data["last_run"] is not None:
            data["last_run"]["account_id"] = kwargs.get("account_id")
            self.last_run = Report(data=data["last_run"])


class SISImport(models.Model):
    CSV_IMPORT_TYPE = "instructure_csv"

    import_id = models.IntegerField()
    workflow_state = models.CharField(max_length=100)
    progress = models.CharField(max_length=3)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(SISImport, self).__init__(*args, **kwargs)

        self.import_id = data["id"]
        self.workflow_state = data["workflow_state"]
        self.progress = data.get("progress", "0")
        self.processing_warnings = data.get("processing_warnings", [])
        self.processing_errors = data.get("processing_errors", [])


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

    def __init__(self, *args, **kwargs):
        self.enrollments = []

        data = kwargs.get("data")
        if data is None:
            return super(CanvasUser, self).__init__(*args, **kwargs)

        self.user_id = data["id"]
        self.name = data["name"]
        self.short_name = data.get("short_name")
        self.sortable_name = data.get("sortable_name")
        self.login_id = data.get("login_id")
        self.sis_user_id = data.get("sis_user_id")
        self.email = data.get("email")
        self.time_zone = data.get("time_zone")
        self.locale = data.get("locale")
        self.avatar_url = data.get("avatar_url")
        for enr_datum in data.get("enrollments", []):
            self.enrollments.append(CanvasEnrollment(data=enr_datum))

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

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(Login, self).__init__(*args, **kwargs)

        self.login_id = data["id"]
        self.account_id = data["account_id"]
        self.sis_user_id = data.get("sis_user_id")
        self.unique_id = data["unique_id"]
        self.user_id = data["user_id"]

    def put_data(self):
        return {"login": {"unique_id": self.unique_id,
                          "sis_user_id": self.sis_user_id}}


class CanvasAdmin(models.Model):
    admin_id = models.IntegerField()
    role = models.CharField(max_length=100)
    user = models.ForeignKey(CanvasUser)

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(CanvasAdmin, self).__init__(*args, **kwargs)

        self.admin_id = data["id"]
        self.role = data["role"]
        self.user = CanvasUser(data=data["user"])


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

    def __init__(self, *args, **kwargs):
        self.attachments = []

        data = kwargs.get("data")
        if data is None:
            return super(Submission, self).__init__(*args, **kwargs)

        self.submission_id = data['id']
        self.body = data['body']
        self.attempt = data['attempt']
        if "submitted_at" in data and data["submitted_at"] is not None:
            self.submitted_at = dateutil.parser.parse(data["submitted_at"])
        self.assignment_id = data["assignment_id"]
        self.workflow_state = data["workflow_state"]
        self.preview_url = data["preview_url"]
        self.late = data["late"]
        self.grade = data["grade"]
        self.score = data["score"]
        self.grade_matches_current_submission = data.get(
            "grade_matches_current_submission")
        self.url = data["url"]
        self.grader_id = data["grader_id"]
        if "graded_at" in data and data["graded_at"] is not None:
            self.graded_at = dateutil.parser.parse(data["graded_at"])
        self.submission_type = data["submission_type"]

        for attachment_data in data.get("attachments", []):
            self.attachments.append(Attachment(data=attachment_data))


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
    published = models.NullBooleanField()
    html_url = models.CharField(max_length=500, null=True)
    turnitin_enabled = models.NullBooleanField()
    vericite_enabled = models.NullBooleanField()
    has_submissions = models.NullBooleanField()

    def __init__(self, *args, **kwargs):
        self.submission_types = []
        self.external_tool_tag_attributes = {}

        data = kwargs.get("data")
        if data is None:
            return super(Assignment, self).__init__(*args, **kwargs)

        self.assignment_id = data['id']
        self.course_id = data['course_id']
        self.integration_id = data['integration_id']
        self.integration_data = data['integration_data']
        if 'due_at' in data and data['due_at']:
            self.due_at = dateutil.parser.parse(data['due_at'])
        self.points_possible = data['points_possible']
        self.grading_type = data['grading_type']
        self.grading_standard_id = data['grading_standard_id']
        self.position = data['position']
        self.name = data['name']
        self.muted = data['muted']
        self.published = data['published']
        self.html_url = data['html_url']
        self.turnitin_enabled = data.get('turnitin_enabled', False)
        self.vericite_enabled = data.get('vericite_enabled', False)
        self.has_submissions = data['has_submitted_submissions']
        self.submission_types = data.get('submission_types', [])
        self.external_tool_tag_attributes = data.get(
            'external_tool_tag_attributes', {})

    def json_data(self):
        data = {
            "integration_id": self.integration_id,
            "integration_data": self.integration_data,
        }

        if "external_tool" in self.submission_types:
            data["external_tool_tag_attributes"] = (
                self.external_tool_tag_attributes)

        return {"assignment": data}


class Quiz(models.Model):
    quiz_id = models.IntegerField()
    due_at = models.DateTimeField()
    title = models.CharField(max_length=500)
    html_url = models.CharField(max_length=500, null=True)
    published = models.NullBooleanField()

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(Quiz, self).__init__(*args, **kwargs)

        self.quiz_id = data["id"]
        self.title = data["title"]
        self.html_url = data["html_url"]
        self.published = data["published"]
        self.points_possible = data["points_possible"]
        if "due_at" in data and "due_at" is not None:
            self.due_at = dateutil.parser.parse(data["due_at"])


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

    def __init__(self, *args, **kwargs):
        data = kwargs.get("data")
        if data is None:
            return super(GradingStandard, self).__init__(*args, **kwargs)

        self.grading_standard_id = data["id"]
        self.title = data["title"]
        self.context_type = data["context_type"]
        self.context_id = data["context_id"]
        self.grading_scheme = data["grading_scheme"]


class DiscussionTopic(models.Model):
    topic_id = models.IntegerField()
    html_url = models.CharField(max_length=500, null=True)
    course_id = models.IntegerField()


class DiscussionEntry(models.Model):
    entry_id = models.IntegerField()
    user_id = models.IntegerField()
