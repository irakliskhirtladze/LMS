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


# class AttendanceForm(forms.ModelForm):
#     class Meta:
#         model = Lecture
#         fields = ['subject', 'student']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Customize the student field to render checkboxes
#         self.fields['student'].widget = forms.CheckboxSelectMultiple()
