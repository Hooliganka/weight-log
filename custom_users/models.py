import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = 'site_users'
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    email_key = models.CharField(verbose_name='E-Mail Key', max_length=30, blank=True, null=True)
    token = models.CharField(verbose_name='Код авторизации', max_length=36, blank=True, null=True)

    @property
    def get_token(self):
        self.token = uuid.uuid4().__str__()
        self.save()
        return self.token

    def clear_token(self):
        self.token = None
        self.save()
