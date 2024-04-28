from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from accounts.models import CustomUser


class Faculty(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Faculty name'), unique=True)
    description = models.TextField(verbose_name=_('Description'))

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Subject name'), unique=True)
    description = models.TextField(verbose_name=_('Description'))
    syllabus = models.FileField(verbose_name=_('Syllabus'), upload_to='syllabus/')

    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE, verbose_name=_('Lecturer'))
    faculty = models.ManyToManyField('Faculty', verbose_name=_('Faculty'))
    student = models.ManyToManyField('Student', null=True, blank=True, verbose_name=_('Student'))
    assignment = models.ForeignKey('Assignment',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True,
                                   verbose_name=_('Assignment'))

    class Meta:
        verbose_name = _('Subject')
        verbose_name_plural = _('Subjects')

    def __str__(self):
        return self.name


class Lecturer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    name = models.CharField(max_length=200, verbose_name=_('Lecturer name'))
    surname = models.CharField(max_length=200, verbose_name=_('Lecturer surname'))

    class Meta:
        verbose_name = _('Lecturer')
        verbose_name_plural = _('Lecturers')

    def __str__(self):
        return f'{self.name} {self.surname}'


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True, verbose_name=_('User'))
    name = models.CharField(max_length=200, verbose_name=_('Student name'))
    surname = models.CharField(max_length=200, verbose_name=_('Student surname'))

    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE, verbose_name=_('Faculty'))

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')

    def __str__(self):
        return f'{self.name} {self.surname}'


class Lecture(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name=_('Date'))
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE, verbose_name=_('Subject'))
    student = models.ManyToManyField('Student', verbose_name=_('Students'))

    class Meta:
        verbose_name = _('Lecture')
        verbose_name_plural = _('Lectures')

    def __str__(self):
        return f'{self.date} - {self.subject}'


class Assignment(models.Model):
    description = models.TextField(verbose_name=_('Description'))
    deadline = models.DateTimeField(verbose_name=_('Deadline'))

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def is_past_deadline(self):
        return self.deadline < timezone.now()


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, verbose_name=_('Assignment'))
    student = models.ForeignKey('Student', on_delete=models.CASCADE, verbose_name=_('Student'))
    text_submission = models.TextField(null=True, blank=True, verbose_name=_('Text Response'))
    file_submission = models.FileField(null=True,
                                       blank=True,
                                       verbose_name=_('File Response'),
                                       upload_to='assignment_submissions/')

    class Meta:
        verbose_name = _('Assignment Submission')
        verbose_name_plural = _('Assignment Submissions')

    def __str__(self):
        return f'Submission by {self.student.name} {self.student.surname}'



