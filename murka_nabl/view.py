from django.views.generic import TemplateView


class MyBase(TemplateView):
    def get(self, request, *args, **kwargs):
        kwargs['PATH'] = request.META.get('PATH_INFO')
        return super().get(request, *args, **kwargs)
