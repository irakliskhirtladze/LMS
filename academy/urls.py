from django.urls import path
from academy.views import show_home_page


urlpatterns = [
    path('home', show_home_page, name='home'),
]
