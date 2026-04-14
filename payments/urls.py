from django.urls import path
from .views import (
    CreatePaymentView,
    VerifyPaymentView,
    RazorpayWebhookView,
    MockConfirmPaymentView
)

urlpatterns = [
    path("create/", CreatePaymentView.as_view()),
    path("verify/", VerifyPaymentView.as_view()),
    path("webhook/", RazorpayWebhookView.as_view()),
    path("mock-confirm/", MockConfirmPaymentView.as_view()),
]