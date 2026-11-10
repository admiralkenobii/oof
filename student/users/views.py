
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import UserProfile


from .forms import (
    StudentRegistrationForm,
    TeacherRegistrationForm,
)


def register_student(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "users/register_student.html",
        {"form": form},
    )


def register_teacher(request):
    if request.method == "POST":
        form = TeacherRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("teacher_pending")
    else:
        form = TeacherRegistrationForm()

    return render(
        request,
        "users/register_teacher.html",
        {"form": form},
    )


def teacher_pending(request):
    return render(
        request,
        "users/teacher_pending.html",
    )


class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = "login"


@login_required
def profile(request):
    try:
        user_profile = request.user.profile
    except UserProfile.DoesNotExist:
        user_profile = None

    return render(
        request,
        "users/profile.html",
        {"profile": user_profile},
    )
