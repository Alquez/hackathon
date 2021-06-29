from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from account.send_mail import send_confirmation_email
from . import serializers
from .models import CustomUser

User = get_user_model()

class ProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = serializers.ProfileSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(username=self.request.user.username)

class RegisterApiView(APIView):
    def post(self, request):
        serializer = serializers.RegisterApiSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
               send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': "Succesfulli"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'msg': "Link expired"}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(TokenObtainPairView):
    serializer_class = serializers.LoginSerializer
