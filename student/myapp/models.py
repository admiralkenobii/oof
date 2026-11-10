from datetime import date
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db import models

from django.core.validators import MinValueValidator, MaxValueValidator

class Group(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Mark(models.Model):
    class MarkChoices(models.TextChoices):
        TWO = "2", "неудовлетворительно"
        THREE = "3", "удовлетворительно"
        FOUR = "4", "хорошо"
        FIVE = "5", "отлично"
        FAILED = "не зачтено", "не зачтено"
        PASSED = "зачтено", "зачтено"
        NOT_CERTIFIED = "не аттестовано", "не аттестовано"

    mark = models.CharField(
        max_length=20,
        choices=MarkChoices.choices,
        unique=True,
    )

    def __str__(self):
        return self.mark


class Discipline(models.Model):
    name = models.CharField(max_length=100)

    semester = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "semester"],
                name="unique_discipline_semester",
            )
        ]


    def __str__(self):
        return f"{self.name} (Семестр: {self.semester})"


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)

    student_email = models.EmailField(unique=True)

    birth_date = models.DateField()

    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        related_name="students",
    )

    disciplines = models.ManyToManyField(
        Discipline,
        through="StudentDiscipline",
        related_name="students",
    )


    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.group})"

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)

    teacher_email = models.EmailField(unique=True)
    birth_date = models.DateField()
"""
    disciplines = models.ManyToManyField(
        Discipline,
        through="TeacherDiscipline",
        related_name="teachers",
    )
"""
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name} "

class StudentDiscipline(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="student_disciplines",
    )

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.CASCADE,
        related_name="student_disciplines",
    )

    mark = models.ForeignKey(
        Mark,
        on_delete=models.PROTECT,
        related_name="student_disciplines",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "discipline"],
                name="unique_student_discipline",
            )
        ]

    def __str__(self):
        return f"{self.student} — {self.discipline}: {self.mark}"

