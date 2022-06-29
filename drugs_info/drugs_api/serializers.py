from email.policy import default
from rest_framework import serializers
from drugs_api.models import Drug


class DrugDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Drug
        fields = '__all__'


class DrugsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = ('id', 'name', 'active_ingredient')
