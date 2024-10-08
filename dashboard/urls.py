from django.urls import path
from . import views

urlpatterns = [
    path('predictt/', views.predict2, name='predict2'),
    path('diets/', views.diets, name='diets'),
    path('doctors/', views.doctors, name='doctors'),
    path('contact-doctor/', views.contact_doctor, name='contact_doctor'),
    path('resultt/', views.result2, name='result2'),
    path('logout',views.logout_view,name='logout')
]