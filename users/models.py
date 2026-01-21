from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class EmailVerify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - verification"
    


class PasswordReset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - password_reset"
