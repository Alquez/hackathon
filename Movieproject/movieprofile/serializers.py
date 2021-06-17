from rest_framework import serializers
from .models import *

class ProfileProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileProducer
        fields = '__all__'

class ProfileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCustomer
        fields = '__all__'
