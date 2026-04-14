from datetime import timedelta
from django.utils import timezone
from .models import Subscription


def activate_subscription(payment):
    #  old subscriptions
    Subscription.objects.filter(
        user=payment.user,
        is_active=True
    ).update(is_active=False)

    #  new subscription
    Subscription.objects.create(
        user=payment.user,
        plan=payment.plan,
        start_date=timezone.now(),
        end_date=timezone.now() + timedelta(days=payment.plan.duration_days),
        is_active=True
    )