from django.contrib.auth.models import AbstractUser
from django.db import models


# пользователи
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMINISTRATOR = "administrator", "администратор"
        GUEST = "guest", "гость"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.GUEST,
        verbose_name="Роль",
    )

    def __str__(self):
        return self.username