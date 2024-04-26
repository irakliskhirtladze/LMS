from django.urls import path
from django.contrib.auth.decorators import login_required
from academy.views import show_home_page, choose_subject, remove_subject, save_attendance

urlpatterns = [
    path('home', show_home_page, name='home'),
    path('choose_subject/<int:subject_id>', login_required(choose_subject), name='choose_subject'),
    path('remove_subject/<int:subject_id>', login_required(remove_subject), name='remove_subject'),
    path('save-attendance/<int:subject_id>', login_required(save_attendance), name='save_attendance'),
]
