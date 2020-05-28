from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.services, name='services'),
    path('user-services', views.user_services, name='user-services'),
    path('user-services/delete', views.user_service_delete, name='user-services-delete'),
]