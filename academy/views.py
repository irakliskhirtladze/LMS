from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academy.utils import get_user_role
from academy.models import Subject


@login_required
def show_lecturer_page(request):
    user = request.user
    user_role = get_user_role(user)[0]

    if user_role == 'Lecturer':
        # Show list of subjects and students for each subject
        lecturer = get_user_role(user)[1]
        subjects = Subject.objects.filter(lecturer=lecturer)
        return render(request, 'academy/lecturer.html',
                      {'user_role': user_role, 'user': request.user, 'subjects': subjects})


@login_required
def show_student_page(request):
    user = request.user
    user_role = get_user_role(user)[0]

    if user_role == 'Student':
        # Show list of subjects and a lecturer for each subject
        student = get_user_role(user)[1]
        faculty = student.faculty
        subjects = student.subjects.all()

        return render(request, 'academy/student.html',
                      {'user_role': user_role, 'user': request.user, 'subjects': subjects, 'faculty': faculty})
