from django.urls import path
from drugs_ui import views

urlpatterns = [
    path('<int:pk>', views.index),
    path('add/', views.add_drug, name='add'),
    path('search/<str:search_type>/<str:component>', views.drug_search_by_component),
]
