
University Management System (UMS)
===================================

Overview
--------
The University Management System (UMS) is a Django-based REST API project designed to manage various aspects of a university's operations. 
It supports JWT authentication, Google OAuth login, and includes endpoints for managing users, students, faculty, departments, courses, 
enrollments, attendance, exams, results, assignments, submissions, and notices.

Key Features
------------
- Django 5.x + Django REST Framework (DRF)
- JWT authentication using SimpleJWT
- Google OAuth2 login using dj-rest-auth + django-allauth
- Swagger/OpenAPI documentation
- PostgreSQL database backend
- Modular API endpoints for core university operations

Tech Stack
----------
- Python 3.x
- Django 5.x
- Django REST Framework
- SimpleJWT
- dj-rest-auth
- django-allauth
- drf-yasg (Swagger documentation)
- PostgreSQL

Installation
------------
1. Clone the repository:
```bash
   git clone https://github.com/codebysubhan/university-management-system.git  
   cd university-management-system
```
2. Create and activate a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Configure the database in `settings.py` (default: PostgreSQL):
   Update NAME, USER, PASSWORD, HOST, PORT as per your local setup.

5. Apply migrations:
```bash
   python manage.py migrate
```
6. Create a superuser:
```bash
   python manage.py createsuperuser
```
7. Run the server:
```bash
   python manage.py runserver
```
Authentication
--------------
1. JWT Authentication:
   - Obtain token: POST /api/token/ (username & password)
   - Refresh token: POST /api/token/refresh/

2. Google OAuth2 Login:
   - POST access_token to: /api/auth/social/google/
   - Receives JWT token in response.

API Endpoints
-------------
- User Management: /api/users/
- Students: /api/students/
- Faculty: /api/faculty/
- Departments: /api/departments/
- Courses: /api/courses/
- Enrollments: /api/enrollments/
- Attendance: /api/attendance/
- Exams: /api/exams/
- Results: /api/results/
- Assignments: /api/assignments/
- Submissions: /api/submissions/
- Notices: /api/notices/
- JWT: /api/token/ , /api/token/refresh/
- Google OAuth: /api/auth/social/google/

Swagger Documentation
----------------------
- Available at: /swagger/

Default Credentials
-------------------
- Superuser credentials created during setup.

License
-------
MIT License

Author
------
Subhan Ali


---
### Entity Sets:
1. ***User***  
`user_id` (PK)  
`username`  
`email`  
`password`  
`role` (admin, faculty, student)  
`is_active`
---
3. ***Student***  
`student_id` (PK)  
`user_id` (FK → User.user_id)  
`roll_number` (unique)  
`batch`  
`department_id` (FK → Department.department_id)
---
4. ***Faculty***  
`faculty_id` (PK)  
`user_id` (FK → User.user_id)  
`employee_id` (unique)  
`specialization`  
`department_id` (FK → Department.department_id)
---
5. ***Department***  
`department_id` (PK)  
`name`  
`code`  
`hod_id` (FK → Faculty.faculty_id)
---
6. ***Course***  
`course_id` (PK)  
`code` (unique)  
`name`  
`credits`  
`department_id` (FK → Department.department_id)  
`faculty_id` (FK → Faculty.faculty_id)
---
7. ***Enrollment***  
`enrollment_id` (PK)  
`student_id` (FK → Student.student_id)  
`course_id` (FK → Course.course_id)  
`enrollment_date`  
(Composite Unique: student_id + course_id)
---
8. ***Attendance***  
`attendance_id` (PK)  
`student_id` (FK → Student.student_id)  
`course_id` (FK → Course.course_id)  
`date`  
`status` (present / absent / late)  
(Composite Unique: student_id + course_id + date)
---
9. ***Exam***  
`exam_id` (PK)  
`course_id` (FK → Course.course_id)  
`exam_type` (mid, final, etc.)  
`exam_date`
---
10. ***Result***  
`result_id` (PK)  
`student_id` (FK → Student.student_id)  
`course_id` (FK → Course.course_id)  
`exam_id` (FK → Exam.exam_id)  
`marks`  
`grade`
---
11. ***Assignment***  
`assignment_id` (PK)  
`title`  
`description`  
`due_date`  
`course_id` (FK → Course.course_id)  
`uploaded_by_id` (FK → Faculty.faculty_id or User.user_id)  
`file_path` (optional)
---
12. ***AssignmentSubmission***  
`submission_id` (PK)  
`assignment_id` (FK → Assignment.assignment_id)  
`student_id` (FK → Student.student_id)  
`submitted_on`  
`file_path`  
`remarks`  
(Composite Unique: assignment_id + student_id)
---
13. ***Notice***  
`notice_id` (PK)  
`title`  
`message`  
`created_by_id` (FK → User.user_id)
`to_role` (student, faculty, all)
`timestamp`