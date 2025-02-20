from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.conf import settings
from .forms import RegistrationForm
from .models import UserVerification
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

# Create your views here.
#indexfile
def index1(request):
    return render(request,'index.html')

#aboutfile
def about(request):
    return render(request,'index.html')

#contactfile
def contact(request):
    return render(request,'contact.html')
#blogfile
def blog(request):
    return render(request,'blog.html')

#profilefile
def profile(request):
    return render(request,'profile.html')
#roomfile
def rooms(request):
    return render(request,'rooms.html')
#packagefile
def packages(request):
    return render(request,'packages.html')
#foodfile
def foods(request):
    return render(request,'packages.html')
#
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Use email as username
            user = User(
                username=email,
                email=email,
                is_active=False
            )
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Generate OTP
            otp = ''.join(random.choices('0123456789', k=6))
            
            # Create verification record
            verification = UserVerification.objects.create(
                user=user,
                otp=otp,
                account_type=form.cleaned_data['account_type'],
                expires_at=timezone.now() + timezone.timedelta(minutes=10)
            )

            # Send verification email
            context = {
                'username': user.email,
                'otp': otp
            }
            send_verification_email(user.email, context)
            
            messages.success(request, 'Registration successful! Please check your email for verification.')
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    
    return render(request, 'User/registration.html', {'form': form})

def send_verification_email(email, context):
    subject = 'Welcome to QUANTUM STAY AI - Verify Your Account'
    html_message = render_to_string('emails/verification_email.html', context)
    
    send_mail(
        subject,
        'Please verify your account',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message,
        fail_silently=False,
    )

def verify_otp(request):
    user_id = request.session.get('registration_user_id')
    if not user_id:
        messages.error(request, 'Registration session expired. Please register again.')
        return redirect('registration')

    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            verification = UserVerification.objects.get(
                user_id=user_id,
                otp=otp,
                is_verified=False
            )
            
            # Check if OTP has expired
            if verification.expires_at < timezone.now():
                messages.error(request, 'OTP has expired. Please register again.')
                verification.user.delete()  # Delete unverified user
                return redirect('registration')

            # Verify user
            verification.is_verified = True
            verification.save()
            
            user = verification.user
            user.is_active = True
            user.save()

            # Send welcome email
            context = {
                'username': user.username,
                'account_type': verification.account_type
            }
            welcome_html = render_to_string('emails/welcome_email.html', context)
            send_mail(
                'Welcome to QUANTUM STAY AI',
                'Welcome to our platform',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=welcome_html,
                fail_silently=False,
            )

            messages.success(request, 'Account verified successfully! Please login.')
            return redirect('login')
        except UserVerification.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')

    return render(request, 'User/verify_otp.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index1')
    else:
        form = LoginForm()
    return render(request, 'User/login.html', {'form': form})
def bookingdetails(request):
    return render(request,'packages.html')
def prediction(request):
    return render(request,'packages.html')
def feedback(request):
    return render(request,'packages.html')
def chat(request):
    return render(request,'packages.html')
def chatbot(request):
    return render(request,'packages.html')
def membershpis(request):
    return render(request,'packages.html')

def dynamicprizing(request):
    return render(request,'packages.html')
def paymentdetails(request):
    return render(request,'packages.html')
def cancel(request):
    return render(request,'packages.html')
def refund(request):
    return render(request,'packages.html')
def offers(request):
    return render(request,'packages.html')

