from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from myapp.models import (
    Discipline,
    Group,
    Mark,
    Student,
    StudentDiscipline,
)


class Command(BaseCommand):
    help = (
        "Заполняет БД тестовыми данными, подготовленными "
        "для заданий по ORM-запросам."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Удалить все данные учебного приложения перед заполнением.",
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options["reset"]:
                StudentDiscipline.objects.all().delete()
                Student.objects.all().delete()
                Discipline.objects.all().delete()
                Mark.objects.all().delete()
                Group.objects.all().delete()

            # Группы
            groups = {}

            for group_name in ("310", "310а"):
                group, _ = Group.objects.get_or_create(name=group_name)
                groups[group_name] = group

            # Все возможные оценки из MarkChoices
            marks = {}

            for value, _label in Mark.MarkChoices.choices:
                mark, _ = Mark.objects.get_or_create(mark=value)
                marks[value] = mark

            # Дисциплины
            discipline_data = [
                ("Языки программирования", 1),
                ("Математика", 1),
                ("Иностранный язык", 1),
                ("Информационные системы", 2),
                ("Интернет-программирование", 2),
                ("Алгоритмы и структуры данных", 2),
            ]

            disciplines = {}

            for name, semester in discipline_data:
                discipline, _ = Discipline.objects.get_or_create(
                    name=name,
                    semester=semester,
                )
                disciplines[(name, semester)] = discipline

            student_data = [
                {
                    "first_name": "Анна",
                    "last_name": "Иванова",
                    "middle_name": "Сергеевна",
                    "student_email": "anna.ivanova@sibstrin.ru",
                    "birth_date": date(2006, 5, 30),
                    "group_name": "310",
                },
                {
                    "first_name": "Мария",
                    "last_name": "Соколова",
                    "middle_name": "Олеговна",
                    "student_email": "maria.sokolova@sibstrin.ru",
                    "birth_date": date(2006, 4, 12),
                    "group_name": "310",
                },
                {
                    "first_name": "Павел",
                    "last_name": "Андреев",
                    "middle_name": "Игоревич",
                    "student_email": "pavel.andreev@sibstrin.ru",
                    "birth_date": date(2006, 3, 1),
                    "group_name": "310",
                },
                {
                    "first_name": "Елена",
                    "last_name": "Смирнова",
                    "middle_name": "Викторовна",
                    "student_email": "elena.smirnova@sibstrin.ru",
                    "birth_date": date(2006, 1, 1),
                    "group_name": "310",
                },
                {
                    "first_name": "Иван",
                    "last_name": "Кузнецов",
                    "middle_name": "Андреевич",
                    "student_email": "ivan.kuznetsov@sibstrin.ru",
                    "birth_date": date(2006, 6, 1),
                    "group_name": "310а",
                },

                {
                    "first_name": "Дмитрий",
                    "last_name": "Петров",
                    "middle_name": "Алексеевич",
                    "student_email": "dmitry.petrov@sibstrin.ru",
                    "birth_date": date(2005, 11, 3),
                    "group_name": "310а",
                },
                {
                    "first_name": "Ольга",
                    "last_name": "Васильева",
                    "middle_name": "Николаевна",
                    "student_email": "olga.vasileva@sibstrin.ru",
                    "birth_date": date(2006, 6, 2),
                    "group_name": "310а",
                },
                {
                    "first_name": "Сергей",
                    "last_name": "Орлов",
                    "middle_name": "Павлович",
                    "student_email": "sergey.orlov@sibstrin.ru",
                    "birth_date": date(2005, 12, 31),
                    "group_name": "310а",
                },
            ]

            students = {}

            for data in student_data:
                student, _ = Student.objects.update_or_create(
                    student_email=data["student_email"],
                    defaults={
                        "first_name": data["first_name"],
                        "last_name": data["last_name"],
                        "middle_name": data["middle_name"],
                        "birth_date": data["birth_date"],
                        "group": groups[data["group_name"]],
                    },
                )
                students[data["student_email"]] = student

            student_disciplines = [
                ("anna.ivanova@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.TWO.value),
                ("anna.ivanova@sibstrin.ru", ("Математика", 1), Mark.MarkChoices.FIVE.value),
                ("anna.ivanova@sibstrin.ru", ("Иностранный язык", 1), Mark.MarkChoices.FOUR.value),
                ("anna.ivanova@sibstrin.ru", ("Информационные системы", 2), Mark.MarkChoices.PASSED.value),
                ("anna.ivanova@sibstrin.ru", ("Интернет-программирование", 2), Mark.MarkChoices.FOUR.value),

                ("maria.sokolova@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.TWO.value),
                ("maria.sokolova@sibstrin.ru", ("Математика", 1), Mark.MarkChoices.FOUR.value),
                ("maria.sokolova@sibstrin.ru", ("Иностранный язык", 1), Mark.MarkChoices.PASSED.value),
                ("maria.sokolova@sibstrin.ru", ("Информационные системы", 2), Mark.MarkChoices.FOUR.value),

                ("pavel.andreev@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.THREE.value),
                ("pavel.andreev@sibstrin.ru", ("Математика", 1), Mark.MarkChoices.FIVE.value),
                ("pavel.andreev@sibstrin.ru", ("Иностранный язык", 1), Mark.MarkChoices.FOUR.value),

                ("elena.smirnova@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.TWO.value),
                ("elena.smirnova@sibstrin.ru", ("Иностранный язык", 1), Mark.MarkChoices.THREE.value),
                ("elena.smirnova@sibstrin.ru", ("Интернет-программирование", 2), Mark.MarkChoices.FOUR.value),
                ("elena.smirnova@sibstrin.ru", ("Алгоритмы и структуры данных", 2), Mark.MarkChoices.THREE.value),

                ("ivan.kuznetsov@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.TWO.value),
                ("ivan.kuznetsov@sibstrin.ru", ("Математика", 1), Mark.MarkChoices.THREE.value),
                ("ivan.kuznetsov@sibstrin.ru", ("Информационные системы", 2), Mark.MarkChoices.FIVE.value),
                ("ivan.kuznetsov@sibstrin.ru", ("Интернет-программирование", 2), Mark.MarkChoices.FIVE.value),
                ("ivan.kuznetsov@sibstrin.ru", ("Алгоритмы и структуры данных", 2), Mark.MarkChoices.FOUR.value),

                ("dmitry.petrov@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.FOUR.value),
                ("dmitry.petrov@sibstrin.ru", ("Информационные системы", 2), Mark.MarkChoices.TWO.value),
                ("dmitry.petrov@sibstrin.ru", ("Интернет-программирование", 2), Mark.MarkChoices.FAILED.value),

                ("olga.vasileva@sibstrin.ru", ("Математика", 1), Mark.MarkChoices.FOUR.value),
                ("olga.vasileva@sibstrin.ru", ("Иностранный язык", 1), Mark.MarkChoices.NOT_CERTIFIED.value),

                ("sergey.orlov@sibstrin.ru", ("Языки программирования", 1), Mark.MarkChoices.FIVE.value),
                ("sergey.orlov@sibstrin.ru", ("Иностранный язык", 1), Mark.MarkChoices.FIVE.value),
                ("sergey.orlov@sibstrin.ru", ("Информационные системы", 2), Mark.MarkChoices.FOUR.value),
                ("sergey.orlov@sibstrin.ru", ("Интернет-программирование", 2), Mark.MarkChoices.FIVE.value),
                ("sergey.orlov@sibstrin.ru", ("Алгоритмы и структуры данных", 2), Mark.MarkChoices.PASSED.value),
            ]

            for email, discipline_key, mark_value in student_disciplines:
                StudentDiscipline.objects.update_or_create(
                    student=students[email],
                    discipline=disciplines[discipline_key],
                    defaults={"mark": marks[mark_value]},
                )

        self.stdout.write(
            self.style.SUCCESS(
                "База заполнена успешно: "
                f"групп — {Group.objects.count()}, "
                f"оценок — {Mark.objects.count()}, "
                f"дисциплин — {Discipline.objects.count()}, "
                f"студентов — {Student.objects.count()}, "
                f"записей об успеваемости — {StudentDiscipline.objects.count()}."
            )
        )