from rest_framework import serializers
from .models import Userinfo
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
    # def validate_password(self,value):
    #     if self.pass1 != self.pass2 :
    #      return Response("User password does not match", status=status.HTTP_400_BAD_REQUEST)`

    