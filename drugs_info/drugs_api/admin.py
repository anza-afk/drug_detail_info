from django.contrib import admin
from .models import Drug, DrugLink, ActiveIngredient
admin.site.register(DrugLink)
admin.site.register(Drug)
admin.site.register(ActiveIngredient)
