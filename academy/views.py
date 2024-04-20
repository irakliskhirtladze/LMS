from django.shortcuts import render


def show_faculties(request):

    return render(request, 'academy/faculty.html')
