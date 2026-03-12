from django.contrib import admin
from django.urls import path,include
from .views import *
from .views import StartUpgradeView, ConfirmPaymentView
urlpatterns = [
    


    path("start-upgrade/", StartUpgradeView.as_view()),
    path("confirm-payment/", ConfirmPaymentView.as_view()),


]