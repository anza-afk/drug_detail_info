from django.urls import path
from drugs_ui import views

urlpatterns = [
    path('<int:pk>', views.index),
    path('add/', views.add_drug, name='add'),
]
