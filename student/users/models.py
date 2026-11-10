
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    class Role(models.TextChoices):
        STUDENT = "student", "Студент"
        TEACHER = "teacher", "Преподаватель"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )

    student = models.OneToOneField(
        "myapp.Student",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profile",
    )

    teacher = models.OneToOneField(
        "myapp.Teacher",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profile",
    )

    is_approved = models.BooleanField(
        default=False,
        verbose_name="Подтвержден администратором",
    )

    def __str__(self):
        return f"{self.user.username} — {self.get_role_display()}"

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
