from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Department, Student, Faculty, Course, Enrollment,
    Attendance, Exam, Result, Assignment, AssignmentSubmission, Notice
)


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'hod')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'batch', 'department')


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'specialization', 'department')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'department', 'faculty')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'status')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('course', 'exam_type', 'exam_date')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'exam', 'marks', 'grade')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'due_date', 'uploaded_by')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_on')


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'to_role', 'timestamp')


# Finally register the custom User admin
admin.site.register(User, UserAdmin)
