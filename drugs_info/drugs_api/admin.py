from django.contrib import admin
from .models import Drug, ActiveIngredient

# Register your models here.
admin.site.register(Drug)
admin.site.register(ActiveIngredient)
