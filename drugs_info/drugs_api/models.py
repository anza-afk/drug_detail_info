from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ActiveIngredientManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class ActiveIngredient(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        db_index=True,
        unique=True
    )
    user = models.ForeignKey(
        User,
        verbose_name='user',
        on_delete=models.SET_NULL,
        null=True,
        default=1
    )

    objects = ActiveIngredientManager()

    def __str__(self):
        return self.name


class Drug(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=256,
        db_index=True,
        unique=True
    )
    active_ingredient = models.ManyToManyField(
        ActiveIngredient,
        verbose_name='Действующее вещество',
    )
    pharmacological_class = models.CharField(
        verbose_name = 'Фармакологическая группа',
        max_length=256,
        null=True
    )
    form_of_release = models.CharField(
        'Лекарственная форма',
        max_length=64,
        null=True
    )
    recipe_only = models.BooleanField(
        verbose_name='Требуется рецепт',
        null=True
    )

    # user = models.ForeignKey(
    #     User,
    #     verbose_name='user',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     default='Anon'
    # )


class DrugLink(models.Model):
    url = models.CharField(
        verbose_name='Ссылка',
        max_length=256,
        db_index=True,
        unique=True
    )
    drug_id = models.ForeignKey(
        Drug,
        verbose_name='Лекарство',
        null=True,
        on_delete=models.SET_NULL
    )
