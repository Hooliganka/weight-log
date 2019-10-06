import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from murka_nabl.decors import is_login
from murka_nabl.serializer import Serializer
from weight.models import Weight


class AddWeight(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @is_login
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        if data:
            try:
                Weight.objects.create(
                    weight=data.get('weight_cat', ''),
                    comment=data.get('comments', ''),
                    user=request.user,
                )
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ошибка формата',
                }, status=400)

            return JsonResponse({
                'status': 'ok',
            })

        return JsonResponse({
            'status': 'error',
        }, status=400)


class GetWeight(View):
    @is_login
    def get(self, request, *args, **kwargs):
        s_obj = Serializer(
            Weight.objects.all(),
            (
                'id',
                'user',
                'date',
                'weight',
                'comment',
            )
        )
        return JsonResponse({
            'status': 'ok',
            'data': s_obj.serialize()
        })
