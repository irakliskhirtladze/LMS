from django import forms
from .models import Assignment, AssignmentSubmission
from django.utils.translation import gettext_lazy as _


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }


# class AssignmentSubmissionForm(forms.ModelForm):
#     class Meta:
#         model = AssignmentSubmission
#         fields = ['text_response', 'file_response']
