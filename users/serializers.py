from rest_framework import serializers
import uuid
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from users.models import UserProfile,EmailVerify,PasswordReset
from .services import ALL_ROLES






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password',"confirm_password"]

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


   



class AssignRoleSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    role = serializers.ChoiceField(choices=ALL_ROLES)

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        
        return value


    def validate(self, data):
        user_id = data["user_id"]
        role = data["role"]

        user = User.objects.get(id=user_id)

        if hasattr(user, "profile") and user.profile.role == role:
            raise serializers.ValidationError({
                "role": "User already has this role"
            })

        return data