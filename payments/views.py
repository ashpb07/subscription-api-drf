import os
import json
import razorpay

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Payment, Plan
from .utils import activate_subscription


# 🔹 Create Razorpay Order
class CreatePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not settings.RAZORPAY_KEY_ID:
            return Response(
                {"error": "Payment gateway not configured"},
                status=503
            )

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        plan_id = request.data.get("plan_id")
        plan = Plan.objects.get(id=plan_id)

        order = client.order.create({
            "amount": int(plan.price * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            user=request.user,
            plan=plan,
            amount=plan.price,
            status="pending",
            transaction_id=order["id"]
        )

        return Response({
            "order_id": order["id"],
            "amount": order["amount"],
            "key": settings.RAZORPAY_KEY_ID
        })


# 🔹 Verify Payment (after frontend)
class VerifyPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not settings.RAZORPAY_KEY_ID:
            return Response({"error": "Payment gateway not configured"}, status=503)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        data = {
            "razorpay_order_id": request.data.get("razorpay_order_id"),
            "razorpay_payment_id": request.data.get("razorpay_payment_id"),
            "razorpay_signature": request.data.get("razorpay_signature"),
        }

        try:
            client.utility.verify_payment_signature(data)

            payment = Payment.objects.get(
                transaction_id=data["razorpay_order_id"]
            )

            payment.status = "success"
            payment.save()

            activate_subscription(payment)

            return Response({"status": "success"})

        except Exception:
            return Response({"status": "failed"}, status=400)


# 🔹 Webhook (production)
class RazorpayWebhookView(APIView):

    def post(self, request):
        if not settings.RAZORPAY_KEY_ID:
            return Response({"status": "disabled"})

        payload = request.body
        signature = request.headers.get("X-Razorpay-Signature")

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_webhook_signature(
                payload,
                signature,
                settings.RAZORPAY_WEBHOOK_SECRET
            )

            data = json.loads(payload)

            if data["event"] == "payment.captured":
                order_id = data["payload"]["payment"]["entity"]["order_id"]

                payment = Payment.objects.get(transaction_id=order_id)
                payment.status = "success"
                payment.save()

                activate_subscription(payment)

        except Exception:
            pass

        return Response({"status": "ok"})


# 🔹 MOCK (for testing without Razorpay)
class MockConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("payment_id")

        payment = Payment.objects.get(id=payment_id)

        payment.status = "success"
        payment.transaction_id = "mock_txn"
        payment.save()

        activate_subscription(payment)

        return Response({"status": "mock success"})