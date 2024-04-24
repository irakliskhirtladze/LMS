from django.urls import path
from academy.views import show_home_page, choose_subject, remove_subject, assignment_page, add_assignment


urlpatterns = [
    path('home', show_home_page, name='home'),
    path('choose_subject/<int:subject_id>', choose_subject, name='choose_subject'),
    path('remove_subject/<int:subject_id>', remove_subject, name='remove_subject'),
    path('assignment/<int:subject_id>', assignment_page, name='assignment'),
    path('add_assignment/<int:subject_id>', add_assignment, name='add_assignment'),
]
