from django.urls import path
from . import views

app_name = 'User'

urlpatterns = [
    # 🌍 Main Pages
    path('', views.index, name='index'),
    path('resortindex/', views.resortindex, name='resortindex'),

    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('smart-concierge/',views. smart_concierge, name='smart-concierge'),

    # 🏨 Package Listings
    path('packages/', views.packages, name='packages'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('daycation/', views.daycation, name='daycation'),
    path('staycation/', views.staycation, name='staycation'),
]
