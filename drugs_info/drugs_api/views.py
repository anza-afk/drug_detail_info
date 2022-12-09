from rest_framework import generics
from drugs_api.serializers import DrugDetailSerializer, DrugsListSerializer, DrugsLinksDetailSerializer
from drugs_api.models import Drug, ActiveIngredient
import operator
from django.db.models import Q
from functools import reduce


class CreateDrugView(generics.CreateAPIView):
    serializer_class = DrugDetailSerializer
    # permission_classes = (IsAdminUser, )


class DrugsListView(generics.ListAPIView):
    serializer_class = DrugsListSerializer
    queryset = Drug.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugDetailSerializer
    queryset = Drug.objects.all()
    lookup_field = 'name'
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class DrugsByDrug(generics.ListAPIView):
    serializer_class = DrugsListSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        drug_name = self.request.query_params.get('drug')
        component = self.request.query_params.get('component')
        if drug_name:
            drug = Drug.objects.filter(name__iregex=drug_name).first()
            ingredients = drug.active_ingredient.all()
            query = reduce(operator.or_, (
                Q(name__icontains=item.name) for item in ingredients
            ))
            ingredient_query = ActiveIngredient.objects.filter(query)
        elif component:
            ingredient_query = ActiveIngredient.objects.filter(
                name__iregex=component
            )
        return Drug.objects.filter(active_ingredient__in=ingredient_query)


class CreateDrugLinkView(generics.CreateAPIView):
    serializer_class = DrugsLinksDetailSerializer
