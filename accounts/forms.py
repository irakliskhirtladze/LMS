from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser
from django import forms
from .models import Homework


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class Work(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['description', 'due_date']
