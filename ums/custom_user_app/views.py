from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializer import *
from .permissions import IsAdmin, IsFaculty, IsStudent
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]  # all can see their own

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Student.objects.all()
        if user.role == 'faculty':
            return Student.objects.filter(enrollment__course__faculty__user=user).distinct()
        if user.role == 'student':
            return Student.objects.filter(user=user)
        return Student.objects.none()


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Faculty.objects.all()
        if user.role == 'faculty':
            return Faculty.objects.filter(user=user)
        return Faculty.objects.none()


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Department.objects.all()
        if user.role == 'faculty':
            return Department.objects.filter(faculty__user=user).distinct()
        if user.role == 'student':
            return Department.objects.filter(student__user=user).distinct()
        return Department.objects.none()


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Course.objects.all()
        if user.role == 'faculty':
            return Course.objects.filter(faculty__user=user)
        if user.role == 'student':
            return Course.objects.filter(enrollment__student__user=user).distinct()
        return Course.objects.none()


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Enrollment.objects.all()
        if user.role == 'faculty':
            return Enrollment.objects.filter(course__faculty__user=user)
        if user.role == 'student':
            return Enrollment.objects.filter(student__user=user)
        return Enrollment.objects.none()


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Attendance.objects.all()
        if user.role == 'faculty':
            return Attendance.objects.filter(course__faculty__user=user)
        if user.role == 'student':
            return Attendance.objects.filter(student__user=user)
        return Attendance.objects.none()


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Exam.objects.all()
        if user.role == 'faculty':
            return Exam.objects.filter(course__faculty__user=user)
        if user.role == 'student':
            return Exam.objects.filter(course__enrollment__student__user=user).distinct()
        return Exam.objects.none()


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Result.objects.all()
        if user.role == 'faculty':
            return Result.objects.filter(course__faculty__user=user)
        if user.role == 'student':
            return Result.objects.filter(student__user=user)
        return Result.objects.none()


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Assignment.objects.all()
        if user.role == 'faculty':
            return Assignment.objects.filter(course__faculty__user=user)
        if user.role == 'student':
            return Assignment.objects.filter(course__enrollment__student__user=user).distinct()
        return Assignment.objects.none()


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return AssignmentSubmission.objects.all()
        if user.role == 'faculty':
            return AssignmentSubmission.objects.filter(assignment__course__faculty__user=user)
        if user.role == 'student':
            return AssignmentSubmission.objects.filter(student__user=user)
        return AssignmentSubmission.objects.none()


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsFaculty | IsStudent]

    def get_queryset(self):
        user = self.request.user
        qs = Notice.objects.all()
        if user.role == 'admin':
            return qs
        if user.role == 'faculty':
            return qs.filter(to_role__in=['faculty', 'all'])
        if user.role == 'student':
            return qs.filter(to_role__in=['student', 'all'])
        return Notice.objects.none()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

@method_decorator(csrf_exempt, name='dispatch')
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

    def get_response(self):
        # Let dj-rest-auth handle user creation/login
        original_response = super().get_response()

        # Get the logged in user
        user = self.user  # from SocialLoginView

        # Generate JWT tokens for that user
        refresh = RefreshToken.for_user(user)
        data = {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
        return Response(data)
