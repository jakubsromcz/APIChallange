from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', 'countryCode', 'createdAt', 'groupId']
        extra_kwargs = {
            'name': {'required': True}, # in POST and PUT is required
            'countryCode': {'required': True} # in POST and PUT is requied
        }