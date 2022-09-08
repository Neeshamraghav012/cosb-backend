from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # ...
        return token


def passwordLength(value):
    if len(value) < 6:
        raise serializers.ValidationError('Password length must be atleast 6 characters.')

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length = 255, validators = [passwordLength])


    class Meta:
        model = User
        fields = ('username', 'password', 'email')


    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'], email = validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')