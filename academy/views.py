from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from academy.utils import get_user_role
from academy.models import Subject, Lecture, Assignment, AssignmentSubmission, Student
from academy.forms import AssignmentForm, AssignmentSubmissionForm
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView


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


class SubjectDetailsView(DetailView):
    model = Subject
    template_name = 'academy/subject_details.html'


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


def remove_subject(request, subject_id):
    """Allows a student to remove already chosen subject."""
    if request.method == 'POST':
        subject = get_object_or_404(Subject, pk=subject_id)
        student = request.user.student
        subject.student.remove(student)
        return redirect('home')


class StudentsListView(ListView):
    """Display list of students for a subject"""
    model = Subject
    template_name = 'academy/lecture.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subject = Subject.objects.get(pk=self.kwargs['pk'])
        context['subject'] = subject
        context['students'] = subject.student.all()
        context['subject_id'] = self.kwargs['pk']
        context['date'] = date.today()
        return context


def save_attendance(request, subject_id):
    if request.method == 'POST':
        today = date.today()
        subject = get_object_or_404(Subject, pk=subject_id)
        selected_students_pks = request.POST.getlist('selected_students')
        selected_students = Student.objects.filter(pk__in=selected_students_pks)
        lecture_exists = Lecture.objects.filter(subject=subject, date=today).exists()

        if not lecture_exists:  # Create a new lecture only if it doesn't exist
            lecture = Lecture.objects.create(subject=subject, date=today)
            lecture.student.set(selected_students)
            return redirect('home')

        return redirect('lecture', subject_id)

    return render(request, 'academy/lecture.html')


def show_assignment_page(request, subject_id):
    """Display assignment page"""
    user_role = get_user_role(request.user)[0]

    # Content for lecturer
    if user_role == 'Lecturer':
        subject = get_object_or_404(Subject, pk=subject_id)
        assignment = subject.assignment
        if assignment is None:
            form = AssignmentForm(request.POST)
            return render(request,
                          'academy/assignment.html',
                          {'user_role': user_role, 'subject': subject, 'assignment': assignment, 'form': form})
        if assignment is not None:
            form = AssignmentForm(request.POST, instance=assignment)
            return render(request,
                          'academy/assignment.html',
                          {'user_role': user_role, 'subject': subject, 'assignment': assignment, 'form': form})

    # Content for student
    if user_role == 'Student':
        subject = get_object_or_404(Subject, pk=subject_id)
        assignment = subject.assignment
        submission_exists = AssignmentSubmission.objects.filter(student=request.user.student,
                                                                assignment=assignment).exists()

        print(f'submission_exists: {submission_exists}')

        if assignment is None:
            return render(request, 'academy/assignment.html', {'user_role': user_role, 'subject': subject})

        if assignment is not None:
            form = AssignmentSubmissionForm(request.POST)
            return render(request,
                          'academy/assignment.html',
                          {'user_role': user_role, 'subject': subject, 'assignment': assignment,
                           'submission_exists': submission_exists, 'form': form})


def add_assignment(request, subject_id):
    """Allows a Lecturer to add an assignment"""
    if request.method == 'POST':
        subject = get_object_or_404(Subject, pk=subject_id)
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            subject.assignment = assignment
            subject.save()
            return redirect('home')

    form = AssignmentForm()
    return render(request, 'assignment.html', {'form': form})


class DeleteAssignmentView(DeleteView):
    """Allows a Lecturer to delete an assignment"""
    model = Assignment
    success_url = reverse_lazy('home')


def submit_assignment(request, assignment_id):
    """Allow a student to submit an assignment with a file or text response"""
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=assignment_id)
        form = AssignmentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            assignment_submission = form.save(commit=False)
            assignment_submission.student = request.user.student
            assignment_submission.assignment = assignment
            assignment_submission.save()
            return redirect('home')

    form = AssignmentSubmissionForm()
    return render(request, 'academy/assignment.html', {'form': form})
