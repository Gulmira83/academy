from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('signup/<int:id>', views.signup, name='signup'),
    path('disabled', views.signup, name='signup'),
    path('update-info', views.update_info, name='update_info'),  
    path('debug', views.debug, name='debug'),  
    path('coming-soon', views.commin_soon, name='comming-soon'),  
    path('newsletter', views.newsletter, name='newsletter'),
    path('password/', views.change_password, name='edit-password'),
    path('faq', views.faq, name='faq'),
    path('faq-success', views.faq_success, name='faq_success'),
    path('faq-review',views.faq_review,name='faq_review'),

]