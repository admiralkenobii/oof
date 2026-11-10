
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user","role","student","teacher","is_approved",)

    list_filter = ("role", "is_approved")

    search_fields = ("user__username","user__email","student__last_name","teacher__last_name",)

    list_editable = ("is_approved",)

    readonly_fields = ("user", "role", "student", "teacher")
