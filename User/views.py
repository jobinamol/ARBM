from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from .models import *
from .forms import UserLoginForm, UserRegistrationForm, OTPVerificationForm
from .utils import generate_otp, send_otp_email
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect

# Create your views here.

def index(request):
    # Get featured packages for homepage
    featured_packages = Package.objects.filter(is_featured=True)[:6]
    context = {
        'featured_packages': featured_packages,
    }
    return render(request, 'index.html', context)
def resortindex(request):
    # Get featured packages for homepage
    featured_packages = Package.objects.filter(is_featured=True)[:6]
    context = {
        'featured_packages': featured_packages,
    }
    return render(request, 'resortindex.html', context)

def packages(request):
    # Get filters from request
    package_type = request.GET.get('type')
    price_range = request.GET.get('price')
    duration = request.GET.get('duration')
    
    # Start with all packages
    packages_list = Package.objects.all()
    
    # Apply filters if they exist
    if package_type:
        packages_list = packages_list.filter(type=package_type)
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        packages_list = packages_list.filter(price__gte=min_price, price__lte=max_price)
    if duration:
        packages_list = packages_list.filter(duration=duration)
    
    # Pagination
    paginator = Paginator(packages_list, 9)  # Show 9 packages per page
    page = request.GET.get('page')
    packages = paginator.get_page(page)
    
    context = {
        'packages': packages,
        'package_types': Package.TYPE_CHOICES,
        'price_ranges': [
            {'value': '0-100', 'label': '$0 - $100'},
            {'value': '100-300', 'label': '$100 - $300'},
            {'value': '300-1000', 'label': '$300+'},
        ],
        'durations': Package.DURATION_CHOICES,
    }
    return render(request, 'packages.html', context)

def package_detail(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    context = {
        'package': package,
    }
    return render(request, 'package_detail.html', context)

def daycation(request):
    # Get all daycation packages
    packages_list = Package.objects.filter(type='daycation')
    paginator = Paginator(packages_list, 9)
    page = request.GET.get('page')
    packages = paginator.get_page(page)
    
    context = {
        'packages': packages,
        'package_type': 'Daycation'
    }
    return render(request, 'packages.html', context)

def staycation(request):
    # Get all staycation packages
    packages_list = Package.objects.filter(type='staycation')
    paginator = Paginator(packages_list, 9)
    page = request.GET.get('page')
    packages = paginator.get_page(page)
    
    context = {
        'packages': packages,
        'package_type': 'Staycation'
    }
    return render(request, 'packages.html', context)

@login_required
def profile(request):
    # Get user's bookings and preferences
    bookings = request.user.bookings.all()
    context = {
        'bookings': bookings,
    }
    return render(request, 'profile.html', context)

@login_required
def bookings(request):
    # Get user's bookings
    user_bookings = request.user.bookings.all().order_by('-created_at')
    context = {
        'bookings': user_bookings,
    }
    return render(request, 'bookings.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        # Add contact form handling logic here
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('User:contact')
    return render(request, 'contact.html')

@login_required
def smart_concierge(request):
    context = {
        'title': 'AI Smart Concierge',
        'active_page': 'smart-concierge'
    }
    return render(request, 'smart_concierge.html', context)

def login_select(request):
    return render(request, 'authentication/login_select.html')

def guest_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('User:index')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return render(request, 'authentication/guest_login.html')

def resort_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:  # Check if user is resort staff
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('User:resort_dashboard')
            else:
                messages.error(request, 'Invalid credentials or insufficient permissions.')
    else:
        form = UserLoginForm()
    return render(request, 'authentication/resort_login.html', {'form': form})

def register_select(request):
    return render(request, 'authentication/register_select.html')

def guest_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('User:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/guest_register.html', {'form': form})

def resort_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True  # Mark as resort staff
            user.save()
            messages.success(request, 'Resort registration successful!')
            return redirect('User:resort_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/resort_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('User:index')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email.')
    
    return render(request, 'authentication/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create inactive user
            user = form.save(commit=False)
            user.is_active = False
            user.username = form.cleaned_data['email']
            user.save()

            # Create user profile
            phone_number = form.cleaned_data['phone_number']
            UserProfile.objects.create(
                user=user,
                phone_number=phone_number
            )

            # Generate and save OTP
            otp = generate_otp()
            OTP.objects.create(
                user=user,
                otp=otp,
                purpose='email'
            )

            # Send OTP email
            send_otp_email(user, otp)

            # Store user ID in session
            request.session['registration_user_id'] = user.id
            messages.success(request, 'Please check your email for OTP verification.')
            return redirect('User:verify_otp')
    else:
        form = UserRegistrationForm()
    return render(request, 'authentication/register.html', {'form': form})

def verify_otp(request):
    user_id = request.session.get('registration_user_id')
    if not user_id:
        messages.error(request, 'Invalid session. Please register again.')
        return redirect('User:register')

    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            try:
                user = User.objects.get(id=user_id)
                otp_obj = OTP.objects.filter(
                    user=user,
                    purpose='email',
                    is_verified=False
                ).latest('created_at')

                if otp_obj.is_expired():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return redirect('User:verify_otp')

                if otp_obj.otp == otp:
                    # Activate user
                    user.is_active = True
                    user.save()

                    # Update profile
                    profile = user.userprofile
                    profile.is_email_verified = True
                    profile.save()

                    # Mark OTP as verified
                    otp_obj.is_verified = True
                    otp_obj.save()

                    # Clear session
                    del request.session['registration_user_id']

                    messages.success(request, 'Email verified successfully. Please login.')
                    return redirect('User:login')
                else:
                    messages.error(request, 'Invalid OTP.')
            except (User.DoesNotExist, OTP.DoesNotExist):
                messages.error(request, 'Invalid OTP verification request.')
                return redirect('User:register')
    else:
        form = OTPVerificationForm()

    return render(request, 'authentication/verify_otp.html', {'form': form})

def resend_otp(request):
    user_id = request.session.get('registration_user_id')
    if not user_id:
        messages.error(request, 'Invalid session. Please register again.')
        return redirect('User:register')

    try:
        user = User.objects.get(id=user_id)
        otp = generate_otp()
        OTP.objects.create(
            user=user,
            otp=otp,
            purpose='email'
        )
        send_otp_email(user, otp)
        messages.success(request, 'New OTP has been sent to your email.')
    except User.DoesNotExist:
        messages.error(request, 'Invalid user. Please register again.')
        return redirect('User:register')

    return redirect('User:verify_otp')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('User:index')
