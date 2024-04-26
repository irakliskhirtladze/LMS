## LMS (Learning Management System) [DB Architecture]
1. This project aims to develop a Learning Management System (LMS) using Django, focusing on the database architecture. The system will support the management of students, lecturers, subjects, and faculties.

Features
* Student, Lecturer, Subject, and Faculty objects.
* Adding subjects with title, short description, and syllabus upload.
* Assigning lecturers to subjects.
* Subjects related to faculties, supporting multiple faculties.
* Adding students with personal data and faculty affiliation.
* Student enrollment in subjects, limited to a maximum of 7 subjects.
* Interface for students to select subjects relevant to their faculty.


2. Features
* Task Creation by Lecturer: Lecturers can create tasks by providing simple information such as text description and execution date.
* Assignment Submission by Students: Students can attach assignments by uploading files and/or writing text. These submissions are sent to the lecturer for review.
* Attendance Recording: Lecturers have the ability to record student attendance. This feature allows the lecturer to mark students present for a specific date.
* Subject-wise Attendance Management: A new page is introduced where users can select a subject. Upon selection, users are redirected to a page displaying a list of students enrolled in that subject. A checkbox is provided next to each student's name, allowing the lecturer to mark attendance. The attendance list, along with the date, is saved for future reference.
