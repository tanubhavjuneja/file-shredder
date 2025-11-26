# backend/api/urls.py
from django.urls import path
from .views import contact_form

urlpatterns = [
    path('contact/', contact_form, name='contact_form'),
]