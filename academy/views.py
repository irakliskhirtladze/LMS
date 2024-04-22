from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from academy.utils import get_user_role
from academy.models import Subject


@login_required
def show_home_page(request):
    """Display academy home page when user is logged in (this is different from index page).

    The user role can be 'Student', 'Lecturer' or something else, like admin.

    The page will show the content depending on the user role"""
    user_role = get_user_role(request.user)[0]

    if user_role == 'Lecturer':
        # Show list of subjects and students for each subject
        lecturer = get_user_role(request.user)[1]
        subjects = Subject.objects.filter(lecturer=lecturer)
        return render(request, 'academy/home.html',
                      {'user_role': user_role, 'user': request.user, 'subjects': subjects})

    if user_role == 'Student':
        # Show list of subjects and a lecturer for each subject
        student = get_user_role(request.user)[1]
        faculty = student.faculty
        chosen_subjects = student.subject_set.all()
        available_subjects = Subject.objects.filter(faculty=faculty)

        return render(request,
                      'academy/home.html',
                      {
                          'user_role': user_role,
                          'user': request.user,
                          'faculty': faculty,
                          'chosen_subjects': chosen_subjects,
                          'available_subjects': available_subjects
                      }
                      )
    return render(request, 'academy/home.html', {'user_role': user_role, 'user': request.user})


@login_required
def choose_subject(request, subject_id):
    """Allows a student to choose at most 7 subjects"""
    if request.method == 'POST':
        student = request.user.student
        subject = get_object_or_404(Subject, pk=subject_id)

        # Check if the student has already chosen the maximum number of subjects
        if student.subject_set.count() >= 7:
            messages.error(request, 'You have already chosen the maximum number of subjects.')
            return redirect('home')  # Redirect to a suitable page

        # Check if the student has already chosen this subject
        if student.subject_set.filter(pk=subject_id).exists():
            messages.error(request, 'You have already chosen this subject.')
            return redirect('home')  # Redirect to a suitable page

        # Add the student to the subject's students
        subject.student.add(student)
        messages.success(request, f'Subject "{subject.name}" chosen successfully.')

    return redirect('home')


@login_required
def remove_subject(request, subject_id):
    """Allows a student to remove already chosen subject."""
    if request.method == 'POST':
        subject = get_object_or_404(Subject, pk=subject_id)
        student = request.user.student
        subject.student.remove(student)
        return redirect('home')
