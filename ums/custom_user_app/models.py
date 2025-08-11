from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='student', **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.pop('role', None)
        return self.create_user(username, email, password, role='admin', **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
    ]

    # user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    hod = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True, related_name='headed_departments')

    def __str__(self):
        return self.name

class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    batch = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.roll_number

class Faculty(models.Model):
    faculty_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='faculty_members')

    def __str__(self):
        return self.employee_id

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField()

    class Meta:
        unique_together = ('student', 'course')

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])

    class Meta:
        unique_together = ('student', 'course', 'date')

class Exam(models.Model):
    exam_id = models.AutoField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.course.name} - {self.exam_type} ({self.exam_date})"


class Result(models.Model):
    result_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    marks = models.FloatField()
    grade = models.CharField(max_length=5)

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    uploaded_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    file_path = models.FileField(upload_to='assignments/', null=True, blank=True)
    def __str__(self):
        return f"{self.title} - {self.course.name}"

class AssignmentSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_on = models.DateField()
    file_path = models.FileField(upload_to='submissions/')
    remarks = models.TextField()

    class Meta:
        unique_together = ('assignment', 'student')

class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    to_role = models.CharField(max_length=20, choices=[('student', 'Student'), ('faculty', 'Faculty'), ('all', 'All')])
    timestamp = models.DateTimeField(auto_now_add=True)
