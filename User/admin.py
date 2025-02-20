from django.contrib import admin
from .models import *

class PackageImageInline(admin.TabularInline):
    model = PackageImage
    extra = 1

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price', 'duration', 'is_featured')
    list_filter = ('type', 'duration', 'is_featured')
    search_fields = ('name', 'description')
    inlines = [PackageImageInline]

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)
