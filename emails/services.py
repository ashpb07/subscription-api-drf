from django.core.mail import EmailMessage
from django.conf import settings

def send_verification_email(user, token):
    verify_url = f"http://127.0.0.1:8000/api/users/verify/?token={token}"

    subject = "Verify your email"
    body = f"Hello {user.username},\n\nClick the link to verify:\n{verify_url}"

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.send()



def send_password_reset_email(user, token):
    verify_url = f"http://127.0.0.1:8000/api/users/profile/password/reset/?token={token}"

    subject = "Password reset"
    body = f"Hello {user.username},\n\nClick the link to change your password:\n{verify_url}"

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )

    email.send()
