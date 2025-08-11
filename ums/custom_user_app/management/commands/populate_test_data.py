from django.core.management.base import BaseCommand
from faker import Faker
import random
from datetime import timedelta
from django.utils import timezone

from custom_user_app.models import (
    User, Student, Faculty, Department, Course,
    Enrollment, Attendance, Exam, Result,
    Assignment, AssignmentSubmission, Notice
)

fake = Faker()

class Command(BaseCommand):
    help = "Populate database with bulk test data"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Deleting old data..."))
        AssignmentSubmission.objects.all().delete()
        Assignment.objects.all().delete()
        Result.objects.all().delete()
        Exam.objects.all().delete()
        Attendance.objects.all().delete()
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        Faculty.objects.all().delete()
        Student.objects.all().delete()
        Department.objects.all().delete()
        User.objects.all().delete()
        Notice.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Creating departments..."))
        departments = [
            Department(name=f"{fake.word().capitalize()} Department", code=f"DPT{100+i}")
            for i in range(5)
        ]
        Department.objects.bulk_create(departments)
        departments = list(Department.objects.all())

        self.stdout.write(self.style.SUCCESS("Creating admin users..."))
        admins = [
            User(username=f"admin{i}", email=f"admin{i}@uni.com", role="admin", is_staff=True, is_active=True)
            for i in range(2)
        ]
        for u in admins:
            u.set_password("adminpass123")
        User.objects.bulk_create(admins)

        self.stdout.write(self.style.SUCCESS("Creating faculty users..."))
        faculty_users = [
            User(username=f"faculty{i}", email=f"faculty{i}@uni.com", role="faculty", is_staff=True, is_active=True)
            for i in range(10)
        ]
        for u in faculty_users:
            u.set_password("facultypass123")
        User.objects.bulk_create(faculty_users)
        faculty_users = list(User.objects.filter(role="faculty"))

        self.stdout.write(self.style.SUCCESS("Creating faculty profiles..."))
        faculties = [
            Faculty(
                user=faculty_users[i],
                employee_id=f"EMP{i+1:03}",
                specialization=fake.job(),
                department=random.choice(departments)
            )
            for i in range(len(faculty_users))
        ]
        Faculty.objects.bulk_create(faculties)
        faculties = list(Faculty.objects.all())

        self.stdout.write(self.style.SUCCESS("Assigning HODs..."))
        for dept in departments:
            dept.hod = random.choice(faculties)
            dept.save()

        self.stdout.write(self.style.SUCCESS("Creating student users..."))
        student_users = [
            User(username=f"student{i}", email=f"student{i}@uni.com", role="student", is_active=True)
            for i in range(50)
        ]
        for u in student_users:
            u.set_password("studentpass123")
        User.objects.bulk_create(student_users)
        student_users = list(User.objects.filter(role="student"))

        self.stdout.write(self.style.SUCCESS("Creating student profiles..."))
        students = [
            Student(
                user=student_users[i],
                roll_number=f"ROLL{2000+i}",
                batch=f"{random.randint(2019,2023)}",
                department=random.choice(departments)
            )
            for i in range(len(student_users))
        ]
        Student.objects.bulk_create(students)
        students = list(Student.objects.all())

        self.stdout.write(self.style.SUCCESS("Creating courses..."))
        courses = [
            Course(
                code=f"CSE{100+i}",
                name=fake.catch_phrase(),
                credits=random.randint(2,5),
                department=random.choice(departments),
                faculty=random.choice(faculties)
            )
            for i in range(15)
        ]
        Course.objects.bulk_create(courses)
        courses = list(Course.objects.all())

        self.stdout.write(self.style.SUCCESS("Creating enrollments..."))
        enrollments = []
        for student in students:
            for course in random.sample(courses, k=random.randint(3,6)):
                enrollments.append(Enrollment(
                    student=student,
                    course=course,
                    enrollment_date=fake.date_this_decade()
                ))
        Enrollment.objects.bulk_create(enrollments)

        self.stdout.write(self.style.SUCCESS("Creating attendance records..."))
        attendance_records = []
        seen_attendance = set()
        for enrollment in Enrollment.objects.all():
            for _ in range(5):
                date = fake.date_this_year()
                key = (enrollment.student_id, enrollment.course_id, date)
                if key in seen_attendance:
                    continue
                seen_attendance.add(key)
                attendance_records.append(Attendance(
                    student=enrollment.student,
                    course=enrollment.course,
                    date=date,
                    status=random.choice(['present', 'absent', 'late'])
                ))
        Attendance.objects.bulk_create(attendance_records)

        self.stdout.write(self.style.SUCCESS("Creating exams..."))
        exams = [
            Exam(
                course=random.choice(courses),
                exam_type=random.choice(['mid', 'final']),
                exam_date=fake.date_this_year()
            )
            for _ in range(20)
        ]
        Exam.objects.bulk_create(exams)
        exams = list(Exam.objects.all())

        self.stdout.write(self.style.SUCCESS("Creating results..."))
        results = []
        for exam in exams:
            enrolled_students = Enrollment.objects.filter(course=exam.course)
            for enrollment in enrolled_students:
                results.append(Result(
                    student=enrollment.student,
                    course=exam.course,
                    exam=exam,
                    marks=random.uniform(50,100),
                    grade=random.choice(['A', 'B', 'C', 'D'])
                ))
        Result.objects.bulk_create(results)

        self.stdout.write(self.style.SUCCESS("Creating assignments..."))
        assignments = [
            Assignment(
                title=fake.sentence(),
                description=fake.text(),
                due_date=fake.date_between(start_date="today", end_date="+30d"),
                course=random.choice(courses),
                uploaded_by=random.choice(faculties)
            )
            for _ in range(20)
        ]
        Assignment.objects.bulk_create(assignments)
        assignments = list(Assignment.objects.all())

        self.stdout.write(self.style.SUCCESS("Creating assignment submissions..."))
        submissions = []
        for assignment in assignments:
            enrolled_students = Enrollment.objects.filter(course=assignment.course)
            for enrollment in random.sample(list(enrolled_students), k=min(5, enrolled_students.count())):
                submissions.append(AssignmentSubmission(
                    assignment=assignment,
                    student=enrollment.student,
                    submitted_on=fake.date_this_year(),
                    file_path="submissions/sample.pdf",
                    remarks=fake.sentence()
                ))
        AssignmentSubmission.objects.bulk_create(submissions)

        self.stdout.write(self.style.SUCCESS("Creating notices..."))
        notices = [
            Notice(
                title=fake.sentence(),
                message=fake.text(),
                created_by=random.choice(admins),
                to_role=random.choice(['student', 'faculty', 'all'])
            )
            for _ in range(10)
        ]
        Notice.objects.bulk_create(notices)

        self.stdout.write(self.style.SUCCESS("Test data generation completed successfully!"))
