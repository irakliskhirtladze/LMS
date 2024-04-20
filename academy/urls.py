from django.urls import path
from academy.views import show_lecturer_page, show_student_page


urlpatterns = [
    path('lecturer', show_lecturer_page, name='lecturer_page'),
    path('student', show_student_page, name='student_page'),
]
