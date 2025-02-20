from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from datetime import timedelta
import uuid

# ✅ Custom User Model with Unique Email & Phone Verification
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    
    # Fixing related_name conflicts with Django's built-in Group and Permission models
    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email

# ✅ Feature Model (For icons or amenities in packages)
class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)  # FontAwesome or similar icons

    def __str__(self):
        return self.name

# ✅ Package Model (Staycation & Daycation)
class Package(models.Model):
    TYPE_CHOICES = [
        ('daycation', 'Daycation'),
        ('staycation', 'Staycation'),
    ]

    DURATION_CHOICES = [
        ('1day', '1 Day'),
        ('2-3days', '2-3 Days'),
        ('4+days', '4+ Days'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    rating = models.FloatField(default=5.0)  # Changed from DecimalField for performance
    features = models.ManyToManyField(Feature, related_name='packages')
    image = models.ImageField(upload_to='packages/main_images/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# ✅ Package Images (Multiple images for a package)
class PackageImage(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='packages/gallery/')

    def __str__(self):
        return f"Image for {self.package.name}"

# ✅ OTP Model for Secure Email/Phone Verification & Password Reset
class OTP(models.Model):
    PURPOSE_CHOICES = [
        ('email', 'Email Verification'),
        ('phone', 'Phone Verification'),
        ('reset', 'Password Reset'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > (self.created_at + timedelta(minutes=5))

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP for {self.user.email} ({self.purpose})"

# ✅ Booking Model
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking: {self.user.email} - {self.package.name}"

# ✅ Review & Rating Model
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(default=5)  # 1 to 5 stars
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.email} for {self.package.name} - {self.rating}⭐"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=True,
        blank=True
    )
    # ... other fields ...

    def __str__(self):
        return self.user.username
