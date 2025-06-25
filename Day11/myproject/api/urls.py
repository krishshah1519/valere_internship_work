from django.urls import path
from .views import create_customer
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', create_customer),
    path('login/', obtain_auth_token),
]
