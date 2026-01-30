from rest_framework import serializers
import uuid
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.models import UserProfile,EmailVerify,PasswordReset






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        raw_token = str(uuid.uuid4())

      
        EmailVerify.objects.create(
            user=user, 
            email_token=raw_token
        )
        return user
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")

        return attrs

class EmailSerializer(serializers.Serializer):
     
    token = serializers.CharField()

    def validate_token(self, value):
        try:
            token_obj = EmailVerify.objects.get(email_token=value)
        except EmailVerify.DoesNotExist:
            raise serializers.ValidationError("Invalid token")

        self.user = token_obj.user
        return value
              

class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


    def update(self,instance, validated_data):
           
        password = validated_data.pop("password", None)

        if password:
                instance.set_password(password)

                instance.username = validated_data.get("username", instance.username)
                instance.email = validated_data.get("email", instance.email)

                instance.save()
                return instance
        



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()



class PasswordSerializer(serializers.Serializer):
     
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    

    def validate_token(self, value):
        try:
            reset_obj = PasswordReset.objects.get(password_token=value)
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError("Invalid token")

        self.reset_obj = reset_obj
        return value


   
       