from django.urls import path
from drugs_api.views import CreateDrugView, DrugsListView, DrugDetailView, DrugsByActiveIngredientView


urlpatterns = [
    path('drug/create', CreateDrugView.as_view()),
    path('drug/detail/<str:name>', DrugDetailView.as_view()),
    path('all', DrugsListView.as_view()),
    path('<str:component>', DrugsByActiveIngredientView.as_view()),
]
