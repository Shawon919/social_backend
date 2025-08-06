from celery import shared_task
from django.core.mail import send_mail
from .models import OTP
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

@shared_task
def send_email(email, otp):
    try:
        send_mail(
            subject="Send Email",
            message=f'Your OTP is {otp}',
            from_email='noreply@socialmedia.com',  # use a valid email
            recipient_list=[email],
            fail_silently=False,
        )
        print("Email sent to:", email)
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

@shared_task
def delete_otp(email):
    try:
        otp_email = OTP.objects.get(email=email)
        otp_email.otp = ''  # delete the OTP record completely
        otp_email.save()
        print(f"OTP deleted for {email}")
    except OTP.DoesNotExist:
        print(f"No OTP found for email: {email}")
    except Exception as e:
        print(f"Error while deleting OTP for {email}: {e}")




@shared_task
def delete_unverified_users():
    try:
        threshold = timezone.now() - timedelta(minutes=30)
        unverified_users = User.objects.filter(is_active=False, date_joined__lt=threshold)
        count = unverified_users.count()
        unverified_users.delete()
        print(f"Deleted {count} unverified users who registered before {threshold}")
    except Exception as e:
        print(f"Error deleting unverified users: {e}")


@shared_task
def otp_time_out(email):
    try:
        otp_email = OTP.objects.get(email=email)
        otp_email.delete()
        print('deleted successfully')
    except OTP.DoesNotExist:
        print('otp does not exit')