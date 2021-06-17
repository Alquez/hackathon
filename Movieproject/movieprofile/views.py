from rest_framework import generics
from .models import ProfileProducer, ProfileCustomer
from .serializers import ProfileProducerSerializer, ProfileCustomerSerializer

class ProfileProducerListView(generics.ListAPIView):
    queryset = ProfileProducer.objects.all()
    serializer_class = ProfileProducerSerializer

class ProfileProducerDetailView(generics.RetrieveAPIView):
    queryset = ProfileProducer.objects.all()
    serializer_class = ProfileProducerSerializer

class ProfileProducerUpdateView(generics.UpdateAPIView):
    queryset = ProfileProducer.objects.all()
    serializer_class = ProfileProducerSerializer



class ProfileCustomerListView(generics.ListAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer

class ProfileCustomerDetailView(generics.RetrieveAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer

class ProfileCustomerUpdateView(generics.UpdateAPIView):
    queryset = ProfileCustomer.objects.all()
    serializer_class = ProfileCustomerSerializer
