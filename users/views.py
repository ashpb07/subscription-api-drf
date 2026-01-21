from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer,EmailSerializer,ProfileSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserProfile,EmailVerify
from django.core.mail import send_mail,EmailMessage
from core import settings
from rest_framework.permissions import IsAuthenticated


def index(request):
    return HttpResponse("<h1>users")

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user=serializer.save()
            
            token_obj = EmailVerify.objects.get(user=user) 
            token = token_obj.email_token 
            subject="user auth test"
            message="hello,"+user.first_name
            from_email=settings.EMAIL_HOST_USER
            to_list=[user.email]
            email = EmailMessage(
                subject=subject,
                    body='Hello,'+user.first_name+'http://127.0.0.1:8000/api/users/verify?token='+token,
            from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )
            
            
            email.send()
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

        
    

