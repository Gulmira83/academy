from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('paypal/<int:id>', views.index, name='index'), 
    path('complete/', views.paymentComplete, name='complete'),
    path('declined-payment/', views.declinedPayment, name='declined-payment'),
    path('success-payment/',views.successPayment, name='success-payment')
]