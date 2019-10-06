import json
from django.contrib import auth
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from custom_users.models import User


class Logout(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        meta = request.META.get('HTTP_AUTHORIZATION', '')
        try:
            user = User.objects.get(token=meta)
        except User.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Пользователь не найден'
            })
        user.clear_token()

        return JsonResponse({
            'status': 'ok',
        })


@csrf_exempt
def login(request, *args, **kwargs):
    get_user = json.loads(request.body.decode())
    user = auth.authenticate(request, username=get_user.get('username'), password=get_user.get('password'))
    if user:
        token = user.get_token
        response = JsonResponse({
            'status': 'ok',
            'token': token
        })
        response['auth_token'] = token
        return response

    return JsonResponse({
        'status': 'error',
    }, status=400)

