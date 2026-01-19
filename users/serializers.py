from rest_framework import serializers
import uuid
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.models import EmailVerify






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
        raw_token = str(uuid.uuid4())

      
        EmailVerify.objects.create(
            user=user,
            email_token=raw_token
        )
        return user
    
    # def validate_password(self,value):
    #     if self.pass1 != self.pass2 :
    #      return Response("User password does not match", status=status.HTTP_400_BAD_REQUEST)

class EmailSerializer(serializers.Serializer):
     
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            token_obj = EmailVerify.objects.get(email_token=value)
        except EmailVerify.DoesNotExist:
            raise serializers.ValidationError("Invalid token")

        self.user = token_obj.user
        return value
              