from django.urls import path
from django.contrib.auth.decorators import login_required

from academy.views import show_home_page, SubjectDetailsView, choose_subject, remove_subject, show_assignment_page,\
    add_assignment, DeleteAssignmentView, StudentsListView, submit_assignment, save_attendance



urlpatterns = [
    path('home', show_home_page, name='home'),
    path('choose_subject/<int:subject_id>', login_required(choose_subject), name='choose_subject'),
    path('remove_subject/<int:subject_id>', login_required(remove_subject), name='remove_subject'),
    path('lecture/<int:pk>/', login_required(StudentsListView.as_view()), name='lecture'),
    path('subject_details/<int:pk>/', login_required(SubjectDetailsView.as_view()), name='subject_details'),
    path('assignment/<int:subject_id>', login_required(show_assignment_page), name='assignment'),
    path('add_assignment/<int:subject_id>', login_required(add_assignment), name='add_assignment'),
    path('delete_assignment/<int:pk>', login_required(DeleteAssignmentView.as_view()), name='delete_assignment'),
    path('submit_assignment/<int:assignment_id>/', login_required(submit_assignment), name='submit_assignment'),
    path('save-attendance/<int:subject_id>', login_required(save_attendance), name='save_attendance'),
]
