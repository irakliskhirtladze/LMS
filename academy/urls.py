from django.urls import path
from academy.views import show_faculties


urlpatterns = [
    path('home', show_faculties, name='faculty'),
]
