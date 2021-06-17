from django.contrib.auth import get_user_model, authenticate  # нашего юзера Возвращает
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class RegisterApiSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(min_length=8, write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')



    def validate(self, attrs):
        password2 = attrs.pop('password2')
        if attrs.get('password') != password2:
            raise serializers.ValidationError('Password did not match')
        if not attrs.get('password').isalnum():
            raise serializers.ValidationError('Password field must have digits and characters')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        # user.set_password(validated_data['password'])
        # user.save()
        return user

class LoginSerializer(TokenObtainPairSerializer):
    password = serializers.CharField(min_length=6, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.pop('password', None)
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User does not found')
        user = authenticate(username=email, password=password)
        if user and user.is_active:
            refresh = self.get_token(user)
            attrs['refresh'] = str(refresh)
            attrs['access'] = str(refresh.access_token)
        return attrs
