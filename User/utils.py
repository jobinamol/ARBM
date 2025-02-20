import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

def send_otp_email(user, otp):
    subject = 'Email Verification OTP'
    message = f'Your OTP for email verification is: {otp}\nThis OTP will expire in 5 minutes.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list) 