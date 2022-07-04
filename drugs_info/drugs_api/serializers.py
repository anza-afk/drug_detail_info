from rest_framework import serializers
from drugs_api.models import Drug, ActiveIngredient



class ActiveIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActiveIngredient
        fields = '__all__'


class DrugDetailSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    active_ingredient = ActiveIngredientSerializer(read_only=False, many=True)

    def create(self, validated_data):
        active_ingredient_data = validated_data.pop('active_ingredient')
        drug = Drug.objects.create(**validated_data)
        for ingredient in active_ingredient_data:
            ingredient_dict = dict(ingredient)
            instance = ActiveIngredient.objects.create(drug = drug, name = ingredient_dict['name'])
            drug.active_ingredient.add(instance)
        return drug
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Drug
        fields = '__all__'


class DrugsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'active_ingredient')


