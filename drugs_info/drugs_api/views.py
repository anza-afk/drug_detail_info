from rest_framework import generics
from drugs_api.serializers import DrugDetailSerializer, DrugsListSerializer
from drugs_api.models import Drug


class CreateDrugView(generics.CreateAPIView):
    serializer_class = DrugDetailSerializer


class DrugsListView(generics.ListAPIView):
    serializer_class = DrugsListSerializer
    queryset = Drug.objects.all()


class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugDetailSerializer
    queryset = Drug.objects.all()
