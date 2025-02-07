from django.db import models
from django.contrib.auth.models import User

class Feature(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)  # For FontAwesome icons

    def __str__(self):
        return self.name

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
    capacity = models.IntegerField()
    location = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)
    features = models.ManyToManyField(Feature)
    image = models.ImageField(upload_to='packages/')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class PackageImage(models.Model):
    package = models.ForeignKey(Package, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='packages/')
    
    def __str__(self):
        return f"Image for {self.package.name}"
