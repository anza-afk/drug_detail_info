from rest_framework import serializers
from drugs_api.models import Drug, ActiveIngredient


class ActiveIngredientSerializer(serializers.ModelSerializer):
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
        drug = Drug.objects.create(**validated_data)
        for ingredient in active_ingredient_data:
            ingredient_dict = dict(ingredient)
            obj = ActiveIngredient.objects.create(
                name=ingredient_dict['name']
            )
            drug.active_ingredient.add(obj)
        return drug

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
            # instance.active_ingredient.add(obj)
        print(ingredients)
        instance.active_ingredient.set(ingredients)
        instance.save()
        return instance

    class Meta:
        model = Drug
        fields = '__all__'


class DrugsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'active_ingredient')
