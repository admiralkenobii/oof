from django.contrib import admin

from .models import Group, Student, Discipline, StudentDiscipline, Mark

# Register your models here.
admin.site.register(Group)
admin.site.register(Student)
admin.site.register(Discipline)
admin.site.register(StudentDiscipline)
admin.site.register(Mark)