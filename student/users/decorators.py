
from functools import wraps

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import UserProfile

# wraps - декоратор для сохранения атрибутов оригинальной функции
# login_required - декоратор, который проверяет, что пользователь аутентифицирован
# PermissionDenied - исключение, которое вызывается, когда пользователь не имеет разрешения на доступ к ресурсу
# @wraps(view_func) - сохраняет атрибуты оригинальной функции view_func в обертке wrapper

def approved_teacher_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            raise PermissionDenied

        if (
            profile.role != UserProfile.Role.TEACHER
            or not profile.is_approved
        ):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper
