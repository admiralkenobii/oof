
from django.urls import path
from . import views

urlpatterns = [
    path("register/student/", views.register_student, name="register_student",),
    path("register/teacher/", views.register_teacher, name="register_teacher",),
    path("teacher/pending/", views.teacher_pending, name="teacher_pending",),
    path("login/", views.UserLoginView.as_view(), name="login",),
    path("logout/", views.UserLogoutView.as_view(), name="logout",),
    path("profile/", views.profile, name="profile", ),
]
