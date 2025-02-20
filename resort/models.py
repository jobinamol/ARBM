from django.db import models
from django.contrib.auth.models import User
import random
import string
import uuid

# Create your models here.

class UserVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    otp_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    account_type = models.CharField(max_length=20)
    expires_at = models.DateTimeField(null=True)

    @staticmethod
    def generate_otp():
        return ''.join(random.choices(string.digits, k=6))

    def __str__(self):
        return f"Verification for {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=['otp_token'], name='resort_uv_token_idx'),
            models.Index(fields=['user'], name='resort_uv_user_idx'),
        ]
