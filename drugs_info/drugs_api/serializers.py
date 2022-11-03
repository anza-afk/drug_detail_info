from rest_framework import serializers
from drugs_api.models import Drug, ActiveIngredient, DrugLink


class ActiveIngredientSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ActiveIngredient
        fields = '__all__'
        extra_kwargs = {
            'name': {'validators': []},
        }


class DrugDetailSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    active_ingredient = ActiveIngredientSerializer(read_only=False, many=True)

    def create(self, validated_data):
        active_ingredient_data = validated_data.pop('active_ingredient')
        instance = Drug.objects.create(**validated_data)
        ingredients = []
        for ingredient in active_ingredient_data:
            if ActiveIngredient.objects.filter(
                name=dict(ingredient)["name"]
            ):
                obj = ActiveIngredient.objects.get(
                    name=dict(ingredient)["name"]
                )
            else:
                obj = ActiveIngredient.objects.create(
                    **ingredient
                )
            ingredients.append(obj)
        instance.active_ingredient.set(ingredients)
        return instance

    def update(self, instance, validated_data):
        active_ingredient_data = validated_data.pop('active_ingredient')
        instance.name = validated_data.get("name", instance.name)
        instance.minimal_age = validated_data.get(
            "minimal_age",
            instance.minimal_age
        )
        instance.recipe_only = validated_data.get(
            "recipe_only",
            instance.recipe_only
        )
        instance.form_of_release = validated_data.get(
            "form_of_release",
            instance.form_of_release
        )
        ingredients = []
        for ingredient in active_ingredient_data:
            if ActiveIngredient.objects.filter(
                name=dict(ingredient)["name"]
            ):
                obj = ActiveIngredient.objects.get(
                    name=dict(ingredient)["name"]
                )
            else:
                obj = ActiveIngredient.objects.create(
                    **ingredient
                )
            ingredients.append(obj)
        instance.active_ingredient.set(ingredients)
        instance.save()
        return instance

    class Meta:
        model = Drug
        fields = '__all__'


class DrugsListSerializer(serializers.ModelSerializer):
    active_ingredient = ActiveIngredientSerializer(read_only=False, many=True)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Drug
        fields = ('id', 'name', 'active_ingredient', 'pharmacological_class', 'form_of_release', 'recipe_only')


class DrugsLinksDetailSerializer(serializers.ModelSerializer):
    drug_id = serializers.RelatedField(many=False, read_only=True)

    class Meta:
        model = DrugLink
        # fields = ('id', 'url', 'drug_id')
