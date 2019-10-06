from django.contrib import admin
from weight.models import Weight


@admin.register(Weight)
class Admin(admin.ModelAdmin):
    list_display = [
        'user'
        'weight',
        'date',
        'comment',
    ]

