from rest_framework import generics
from drugs_api.serializers import DrugDetailSerializer, DrugsListSerializer
from drugs_api.models import Drug, ActiveIngredient
import operator
from django.db.models import Q
from functools import reduce


class CreateDrugView(generics.CreateAPIView):
    serializer_class = DrugDetailSerializer


class DrugsListView(generics.ListAPIView):
    serializer_class = DrugsListSerializer
    queryset = Drug.objects.all()


class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugDetailSerializer
    queryset = Drug.objects.all()
    lookup_field = 'name'


class DrugsByActiveIngredientView(generics.ListAPIView):
    serializer_class = DrugsListSerializer

    def get_queryset(self):
        component = self.kwargs['component']
        ingredient_query = ActiveIngredient.objects.filter(
            name__icontains=component
        )
        return Drug.objects.filter(active_ingredient__in=ingredient_query)


class DrugsByDrug(generics.ListAPIView):
    serializer_class = DrugsListSerializer

    def get_queryset(self):
        drug_name = self.kwargs['drug']
        drug = Drug.objects.filter(name=drug_name).first()
        ingredients = drug.active_ingredient.all()
        query = reduce(operator.or_, (
            Q(name__icontains=item.name) for item in ingredients
        ))
        ingredient_query = ActiveIngredient.objects.filter(query)
        return Drug.objects.filter(active_ingredient__in=ingredient_query)
