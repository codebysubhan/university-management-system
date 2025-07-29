# University Management System

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