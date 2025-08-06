from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from .models import OTP
from django.contrib.auth import get_user_model

User = get_user_model()




@shared_task
def send_email(email,otp):
    return send_mail(
        subject= "Send Email",
        message= f'your otp is {otp}',
        from_email= 'https://socialmediaAdmin',
        recipient_list=  [email]

    )
print("email sent")



@shared_task
def delete_otp(email):
    try:
        otp_email = OTP.objects.get(email=email)
        otp_email.otp = ''
        otp_email.save()

    except OTP.DoesNotExist:
        print(f"No OTP found for email: {email}")
    except Exception as e:
        print(f"Error while deleting OTP for {email}: {e}")