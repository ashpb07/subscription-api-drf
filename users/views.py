from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


def index(request):
    return HttpResponse("<h1>users")


def register(request):
      if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass2 = request.POST['pass2']
        email = request.POST['email']
        # if User.objects.filter(username=username):
                
        #         # messages.error(request,"username already exists")
        #         return redirect('signup')
        # if User.objects.filter(email=email):
        #     messages.error(request,"email already exists")
        #     return redirect('signup')    

        # if pass1 != pass2:
        #     messages.error(request, "Passwords do not match.")
        #     return redirect('signup')
        

        # if User.objects.filter(username=username).exists():
        #     messages.error(request, "Username already exists.")
        #     return redirect('signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        # Member.objects.create(user=myuser)

        return Response("User sucessfully created", status=status.HTTP_201_CREATED)
        # messages.success(request, "Signup successful!")