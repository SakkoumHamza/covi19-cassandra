# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('auth/',views.auth_view,name='auth'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify_email/<int:user_id>/', views.verify_email_view, name='verify_email')
]
