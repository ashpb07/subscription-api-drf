from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response                
from .serializers import RegisterSerializer,EmailSerializer,ProfileSerializer,PasswordSerializer,ForgotPasswordSerializer
from rest_framework.views import APIView
from emails.services import send_verification_email,send_password_reset_email
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserProfile,EmailVerify,PasswordReset
from core import settings
from rest_framework.permissions import IsAuthenticated
from payments import models
import uuid



def index(request):
    return HttpResponse("<h1>users")

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user=serializer.save()
            
            token_obj = EmailVerify.objects.get(user=user) 
            token = token_obj.email_token 
            send_verification_email(user, token)
            
            return Response(
                {"message": "User Registered Successfully"},
                status=status.HTTP_201_CREATED
            )

        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

class VerifyEmailView(APIView):

    def get(self, request):
        serializer = EmailSerializer(data=request.query_params)
        
        if serializer.is_valid():
            user = serializer.user
            user.email_verified = True
            user.save()

         
            EmailVerify.objects.filter(user=user).delete()

            return Response({"message": "Email Verified"}, status=200)

        return Response(serializer.errors, status=400)

class LogoutView(APIView):
        def post(self, request):
            try:
                refresh_token = request.data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            




class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email
        })


    def patch(self, request):
        serializer = ProfileSerializer(
            instance=request.user.profile,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    



class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
           
            return Response({"message": "If the email exists, a reset link was sent"})

        token = str(uuid.uuid4())

        PasswordReset.objects.create(
            user=user,
            password_token=token
        )

        send_password_reset_email(user, token)

        return Response({"message": "If the email exists, a reset link was sent"})

class PasswordResetView(APIView):
    def post(self, request):
        serializer = PasswordSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        reset_obj = serializer.reset_obj
        user = reset_obj.user
        new_password = serializer.validated_data["password"]

        user.set_password(new_password)
        user.save()

        reset_obj.delete() 

        return Response({"message": "Password reset successful"})

