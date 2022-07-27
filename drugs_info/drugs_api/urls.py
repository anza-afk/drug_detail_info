from django.urls import include, path
from drugs_api.views import *


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('drug/create', CreateDrugView.as_view()),
    path('drug/detail/<str:name>', DrugDetailView.as_view()),
    path('all', DrugsListView.as_view()),
    path('ingredient/<str:component>', DrugsByActiveIngredientView.as_view()),
    path('drug/<str:drug>', DrugsByDrug.as_view()),
]
