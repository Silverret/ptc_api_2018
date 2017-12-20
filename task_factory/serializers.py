from rest_framework import serializers
from task_factory.models import Country

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name', 'code')
        read_only_fields = ('id', 'name', 'code',)
