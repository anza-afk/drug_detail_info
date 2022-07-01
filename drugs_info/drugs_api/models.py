from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Drug(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        db_index=True,
        unique=True
    )
    active_ingredient = models.CharField(
        verbose_name='Действующее вещество',
        max_length=1024
    )
    minimal_age = models.IntegerField(
        verbose_name='Минимальный возраст',
        null=True
    )
    recipe_only = models.BooleanField(
        verbose_name='Требуется рецепт',
        null=True
    )
    form_of_release = models.CharField(
        'Форма выпуска',
        max_length=64,
        null=True
    )
    # user = models.ForeignKey(
    #     User,
    #     verbose_name='user',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     default='Anon'
    # )
