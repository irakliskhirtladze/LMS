from django import forms
from .models import Assignment, AssignmentSubmission, Lecture


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }


class AssignmentSubmissionForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['text_submission', 'file_submission']

