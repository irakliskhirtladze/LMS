from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from accounts.forms import CustomUserCreationForm
from accounts.forms import Work


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


class LogInView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')


def log_out(request):
    logout(request)
    return redirect('index')


def add_homework(request):
    if request.method == 'POST':
        form = Work(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home page or any other page
    else:
        form = Work()
    return render(request, 'academy/add_homework.html', {'form': form})
