from .models import Student, Lecturer


def get_user_role(user):
    try:
        # Try to get a Student instance associated with the user
        student = Student.objects.get(user=user)
        return 'Student', student
    except Exception:
        pass

    try:
        # Try to get a Lecturer instance associated with the user
        lecturer = Lecturer.objects.get(user=user)
        return 'Lecturer', lecturer
    except Exception:
        pass

    # If neither a Student nor a Lecturer instance is found, the user has no role
    return '', ''
