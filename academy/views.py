from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from academy.utils import get_user_role
from academy.models import Subject


@login_required
def show_home_page(request):
    """-Display academy home page when user is logged in (this is different from index page,
    which is shown when user is not logged in).

    -The user role can be 'Student', 'Lecturer' or something else, like admin.

    -The page will show the content depending on the user role"""
    user = request.user
    user_role = get_user_role(user)[0]

    if user_role == 'Lecturer':
        # Show list of subjects and students for each subject
        lecturer = get_user_role(user)[1]
        subjects = Subject.objects.filter(lecturer=lecturer)
        return render(request, 'academy/home.html',
                      {'user_role': user_role, 'user': request.user, 'subjects': subjects})

    if user_role == 'Student':
        # Show list of subjects and a lecturer for each subject
        student = get_user_role(user)[1]
        faculty = student.faculty
        subjects = Subject.objects.filter(faculties=faculty)

        return render(request, 'academy/home.html',
                      {'user_role': user_role, 'user': request.user, 'subjects': subjects, 'faculty': faculty})
