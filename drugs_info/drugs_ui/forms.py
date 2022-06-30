from django import forms


class DrugForm(forms.Form):
    name = forms.CharField(
        label='Наименование',
        max_length=256,
    )
    active_ingredient = forms.JSONField(
        label='Действующее вещество'
    )
    minimal_age = forms.IntegerField(
        label='Минимальный возраст',
    )
    recipe_only = forms.BooleanField(
        label='Требуется рецепт',
    )
    form_of_release = forms.CharField(
        label='Форма выпуска',
        max_length=64,
    )
    # def __init__(self, user, *args,**kwargs):
    #     self.user = user
    #     super(DrugForm, self).__init__(*args, **kwargs)