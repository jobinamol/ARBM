from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index1/',views.index1,name='index1'), 
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('blog/',views.blog,name='blog'), 
    path('profile/',views.profile,name='profile'), 
    path('rooms/',views.rooms,name='rooms'),
    path('packages/',views.packages,name='packages'),
    path('foods/',views.foods,name='foods'),
    path('registration/',views.registration,name='registration'),
    path('login/',views.login,name='login'),
    path('bookingdetails/',views.bookingdetails,name='bookingdetails'),
    path('prediction/',views.prediction,name='prediction'),
    path('feedback/',views.feedback,name='feedback'),
    path('chat/',views.chat,name='chat'),
    path('chatbot/',views.chatbot,name='chatbot'),
    path('membershpis/',views.membershpis,name='membershpis'),
    path('dynamicprizing/',views.dynamicprizing,name='dynamicprizing'),
    path('paymentdetails/',views.paymentdetails,name='paymentdetails'),
    path('cancel/',views.cancel,name='cancel'),
    path('refund/',views.refund,name='refund'),
    path('offers/',views.offers,name='offers'),    
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]