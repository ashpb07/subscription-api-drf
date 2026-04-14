from django.contrib import admin
from django.urls import path,include
from .views import TestPermissionView,TestSubView
urlpatterns = [
    path("test/", TestPermissionView.as_view()),
    path("test1/", TestSubView.as_view()),   

]