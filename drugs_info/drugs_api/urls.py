from django.urls import path
from drugs_api.views import CreateDrugView, DrugsListView, DrugDetailView, DrugsByActiveIngredientView, DrugsByDrug


urlpatterns = [
    path('drug/create', CreateDrugView.as_view()),
    path('drug/detail/<str:name>', DrugDetailView.as_view()),
    path('all', DrugsListView.as_view()),
    path('ingredient/<str:component>', DrugsByActiveIngredientView.as_view()),
    path('drug/<str:drug>', DrugsByDrug.as_view()),
]
