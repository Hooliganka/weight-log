from django.db import models

from custom_users.models import User


class Weight(models.Model):
    class Meta:
        db_table = 'bd_weight'
        verbose_name = 'Вес'
        verbose_name_plural = 'Вес'
        ordering = ('-date',)

    date = models.DateField(verbose_name='Дата взвешивания', auto_now_add=True)
    weight = models.FloatField(verbose_name='Вес Мурки в кг')
    comment = models.TextField(verbose_name='Комментарий если надо', blank=True)
    user = models.ForeignKey(User, verbose_name='Кто добавил', on_delete=models.CASCADE, blank=True, null=True)


