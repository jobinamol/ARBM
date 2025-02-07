from django.urls import path
from . import views

app_name = 'User'

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('packages/', views.packages, name='packages'),
    path('package/<int:package_id>/', views.package_detail, name='package_detail'),
    path('daycation/', views.daycation, name='daycation'),
    path('staycation/', views.staycation, name='staycation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('smart-concierge/', views.smart_concierge, name='smart-concierge'),
    
    # User related pages
    path('profile/', views.profile, name='profile'),
    path('bookings/', views.bookings, name='bookings'),
    
    # Authentication URLs (if you're not using django.contrib.auth.urls)
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
