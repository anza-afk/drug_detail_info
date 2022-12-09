from django.urls import include, path, re_path
from drugs_api.views import CreateDrugView, DrugDetailView, DrugsListView, DrugsByDrug


urlpatterns = [
    # path('auth/', include('rest_framework.urls')),
    # path('/auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('drug/create', CreateDrugView.as_view()),
    path('drug/detail/<str:name>', DrugDetailView.as_view()),
    path('all', DrugsListView.as_view()),
    path('', DrugsByDrug.as_view()),
]
