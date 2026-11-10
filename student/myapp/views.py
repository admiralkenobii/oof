from django.shortcuts import render
from .models import Student, Group, Discipline, Mark
from django.db.models import Q, Count
from datetime import date

# Create your views here.
def home(request):
    context = {}
    return render(request, 'myapp/home.html', context)

def about(request):
    context = {}
    return render(request, 'myapp/about.html', context)

# задание по практике
def task(request):
    # 1.
    # Найти студентов, родившихся c 01.01.2026 по 01.06.2026
    # включительно. Вывести найденных студентов, отсортированных
    # по дате рождения от самых младших к самым старшим.

    students_2006 = (Student.objects.filter(birth_date__range=(
                        date(2006,1,1),
                        date(2006,6,1)))
                     .order_by("-birth_date"))
    # 2.
    # Получить список всех студентов, изучающих определённую
    # дисциплину (например Языки программирования) и получившим
    # за нее оценку 2. Вывести найденных студентов, отсортированных
    # по фамилии, имени, отчеству.

    students_languages = Student.objects.filter(student_disciplines__discipline__name="Языки программирования",
                                                student_disciplines__mark__mark="2",
                                                ).order_by("last_name", "first_name", "middle_name")

    # 3.
    # Для каждой дисциплины подсчитать количество студентов,
    # изучающих её.

    students_discipline_count = Discipline.objects.annotate(student_count=Count("students"))

    # 4.
    # Найти студентов, у которых есть хотя бы одна оценка «2», но нет
    # оценок «5».

    students_2_but_no_5 = (Student.objects.filter(student_disciplines__mark__mark="2")
                           .exclude(student_disciplines__mark__mark="5"))

    # 5.
    # Получить студентов, изучающих более трёх дисциплин.

    students_more_than_three = (Student.objects.annotate(
                                discipline_count=Count("student_disciplines"))
                                .filter(discipline_count__gt=3))

    context = {
        "students_2006": students_2006,
        "students_languages": students_languages,
        "students_discipline_count": students_discipline_count,
        "students_2_but_no_5": students_2_but_no_5,
        "students_more_than_three": students_more_than_three,
    }
    return render(request, 'myapp/task.html', context)

def students(request):

    # ============================================================
    # 1. ПОЛУЧЕНИЕ ОБЪЕКТОВ
    # ============================================================

    # 1. Все студенты
    students_all = Student.objects.all()

    # 2. Получение одного объекта через get()
    try:
        student_get = Student.objects.get(id=1)
    except Student.DoesNotExist:
        student_get = None

    # 3. Первый и последний студент
    student_first = Student.objects.order_by("last_name").first()
    student_last = Student.objects.order_by("last_name").last()

    # 4. Количество студентов
    students_count = Student.objects.count()


    # ============================================================
    # 2. ФИЛЬТРАЦИЯ
    # ============================================================

    # 5. Фильтрация по группе
    students_filter = Student.objects.filter(
        group__name="410"
    )

    # 6. Исключение группы
    students_exclude = Student.objects.exclude(
        group__name="410"
    )

    # 7. Поиск по части фамилии
    students_contains = Student.objects.filter(
        last_name__icontains="ов"
    )

    # 8. Поиск сразу по нескольким группам
    students_in = Student.objects.filter(
        group__name__in=["410", "416"]
    )

    # 9. Сложное условие через Q()
    students_q = Student.objects.filter(
        Q(group__name="410") |
        Q(group__name="416")
    )


    # ============================================================
    # 3. СОРТИРОВКА И ВЫБОР ПОЛЕЙ
    # ============================================================

    # 10. Сортировка
    students_ordered = Student.objects.order_by(
        "last_name",
        "first_name"
    )

    # 11. values()
    students_values = Student.objects.values(
        "last_name",
        "first_name",
        "student_email",
    )

    # 12. values_list()
    students_values_list = Student.objects.values_list(
        "last_name",
        "first_name",
    )


    # ============================================================
    # 4. СВЯЗИ МЕЖДУ МОДЕЛЯМИ
    # ============================================================

    # 13. select_related()
    students_select_related = Student.objects.select_related(
        "group"
    )

    # 14. prefetch_related()
    students_prefetch = Student.objects.prefetch_related(
        "disciplines"
    )

    # 15. Обратная связь через related_name
    groups = Group.objects.prefetch_related(
        "students"
    )

    # 16. ManyToMany
    students_disciplines = Student.objects.prefetch_related(
        "disciplines"
    )


    # ============================================================
    # 5. АГРЕГАЦИЯ
    # ============================================================

    # 17. Количество дисциплин у каждого студента
    students_annotated = Student.objects.annotate(
        discipline_count=Count("disciplines")
    )

    # 18. Общее количество студентов
    students_aggregate = Student.objects.aggregate(
        total=Count("id")
    )


    # ============================================================
    # 6. QUERYSET И SQL
    # ============================================================

    # 19. Цепочка QuerySet
    students_chain = (
        Student.objects
        .filter(group__name="410")
        .order_by("last_name", "first_name")
    )

    # 20. SQL, который Django построил для QuerySet
    students_sql = students_chain.query


    # ============================================================
    # 7. ДЕМОНСТРАЦИЯ N+1
    # ============================================================

    # Без prefetch_related().
    #
    # В шаблоне при обращении к student.disciplines.all()
    # Django может выполнять дополнительные запросы.
    students_without_prefetch = Student.objects.all()

    # С prefetch_related().
    #
    # Связанные дисциплины загружаются заранее.
    students_with_prefetch = Student.objects.prefetch_related(
        "disciplines"
    )


    # ============================================================
    # CONTEXT
    # ============================================================

    context = {

        # 1–4. Получение объектов
        "students_all": students_all,
        "student_get": student_get,
        "student_first": student_first,
        "student_last": student_last,
        "students_count": students_count,

        # 5–9. Фильтрация
        "students_filter": students_filter,
        "students_exclude": students_exclude,
        "students_contains": students_contains,
        "students_in": students_in,
        "students_q": students_q,

        # 10–12. Сортировка и поля
        "students_ordered": students_ordered,
        "students_values": students_values,
        "students_values_list": students_values_list,

        # 13–16. Связи
        "students_select_related": students_select_related,
        "students_prefetch": students_prefetch,
        "groups": groups,
        "students_disciplines": students_disciplines,

        # 17–18. Агрегация
        "students_annotated": students_annotated,
        "students_aggregate": students_aggregate,

        # 19–20. QuerySet и SQL
        "students_chain": students_chain,
        "students_sql": students_sql,

        # 21. N+1
        "students_without_prefetch": students_without_prefetch,
        "students_with_prefetch": students_with_prefetch,
    }

    return render(
        request,
        "myapp/students.html",
        context,
    )