from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Plan, Subscription, Usage


@receiver(post_save, sender=User)
def create_free_subscription(sender, instance, created, **kwargs):
    if created:
        
        free_plan = Plan.objects.filter(name="free").first()

        if free_plan:
            
            Subscription.objects.create(
                user=instance,
                plan=free_plan,
                start_date=timezone.now(),
                end_date=None,   # Free plan does not expire
                is_active=True,
            )

        
        Usage.objects.create(user=instance)


