from django import forms


class DrugForm(forms.Form):
    name = forms.CharField(
        label='Наименование',
        max_length=256,
    )
    active_ingredient = forms.CharField(
        label='Действующее вещество',
        max_length=1024
    )
    pharmacological_class = forms.CharField(
        label='Фармакологическая группа',
    )
    form_of_release = forms.CharField(
        label='Лекарственная форма',
        max_length=64,
    )
    recipe_only = forms.BooleanField(
        label='Требуется рецепт',
        required=False,
    )
    # def __init__(self, user, *args,**kwargs):
    #     self.user = user
    #     super(DrugForm, self).__init__(*args, **kwargs)