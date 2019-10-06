import functools
from django.http import JsonResponse

from custom_users.models import User


def is_login(method):
    @functools.wraps(method)
    def the_wrapper_around_the_original_function(self, request, *args, **kwargs):
        meta = request.META.get('HTTP_AUTHORIZATION', '')
        try:
            user = User.objects.get(token=meta)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Токен не валиден'
            }, status=400)

        if not user.token:
            return JsonResponse({
                'status': 'error',
                'message': 'Пользователь не авторизирован'
            }, status=400)

        request.user = user
        return method(self, request, *args, **kwargs)

    return the_wrapper_around_the_original_function
