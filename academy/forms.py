from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['description', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'class': 'datetime-input'}),
        }
