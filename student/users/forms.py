
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from myapp.models import Student, Teacher, Discipline
from .models import UserProfile


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    student = forms.ModelChoiceField(
        queryset=Student.objects.filter(
            user_profile__isnull=True
        ),
        label="Студент",
        empty_label="Выберите свою запись",
    )

    class Meta:
        model = User
        fields = ("username", "email", "student")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=UserProfile.Role.STUDENT,
                student=self.cleaned_data["student"],
                is_approved=True,
            )

        return user


class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(
        max_length=100,
        label="Имя",
    )
    last_name = forms.CharField(
        max_length=100,
        label="Фамилия",
    )
    middle_name = forms.CharField(
        max_length=100,
        required=False,
        label="Отчество",
    )
    disciplines = forms.ModelMultipleChoiceField(
        queryset=Discipline.objects.all(),
        required=False,
        label="Преподаваемые дисциплины",
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "disciplines",
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

            teacher = Teacher.objects.create(
                first_name=self.cleaned_data["first_name"],
                last_name=self.cleaned_data["last_name"],
                middle_name=self.cleaned_data["middle_name"],
                teacher_email=self.cleaned_data["email"],
            )
            teacher.disciplines.set(
                self.cleaned_data["disciplines"]
            )

            UserProfile.objects.create(
                user=user,
                role=UserProfile.Role.TEACHER,
                teacher=teacher,
                is_approved=False,
            )

        return user
