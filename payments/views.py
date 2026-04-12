from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Plan, Payment, Subscription
from .serializers import StartUpgradeSerializer
from common.permission import HasSubsription,HasRolePermission



class PlanDetaisView(APIView):
    
    permission_classes = [IsAuthenticated,HasSubsription]
    def get(self, request):
        subscription = request.user.subscription_set.filter(is_active=True).first()

        plan_name = subscription.plan.name if subscription and subscription.plan else None

        if not subscription:
            return Response({"error": "No active subscription"}, status=404)

        start_date =subscription.start_date 
        end_date = subscription.end_date 
        is_active =subscription.is_active
        auto_renew =subscription.auto_renew 

        
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            
            "plan": plan_name,
            "start_date ":start_date,
            "end_date ":end_date ,
            "is_active" :is_active,
           "auto_renew" :auto_renew
    })
    





class StartUpgradeView(APIView):
    permission_classes = [IsAuthenticated,HasSubsription]

    def post(self, request):
        serializer = StartUpgradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_name = serializer.validated_data["plan_name"]

        try:
            plan = Plan.objects.get(name=plan_name)
        except Plan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=404)

        
        payment = Payment.objects.create(
            user=request.user,
            amount=plan.price,
            status="pending",
            transaction_id=f"txn_{timezone.now().timestamp()}",
        )

        return Response({
            "payment_id": payment.id,
            "amount": plan.price,
            "plan": plan.name,
            "message": "Proceed to payment"
        })
    





class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payment_id = request.data.get("payment_id")

        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        if payment.status == "success":
            return Response({"message": "Already confirmed"})

        
        payment.status = "success"
        payment.save()

        subscription = Subscription.objects.get(user=request.user)

    
        plan = Plan.objects.get(price=payment.amount)

        subscription.plan = plan
        subscription.start_date = timezone.now()
        subscription.end_date = timezone.now() + timezone.timedelta(days=30)
        subscription.save()

        return Response({
            "message": "Subscription upgraded",
            "new_plan": plan.name
        })




#test
def index(request):
    return HttpResponse("<h1>pay</h1>")