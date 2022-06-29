from django.urls import path
from drugs_api.views import CreateDrugView, DrugsListView, DrugDetailView


urlpatterns = [
    path('drug/create', CreateDrugView.as_view()),
    path('drug/detail/<int:pk>', DrugDetailView.as_view()),
    path('all', DrugsListView.as_view()),
]
