from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name='sign_up'),
    path("login/", views.log_in, name='login'),
    path("index/", views.index, name='index'),
    path("home/", views.home, name='home'),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path("logout/", views.log_out, name='logout'),
    path("change_password/", views.change_password, name='change_password'),
    path(
        "change_password_form/",
        views.change_password_form,
        name='change_password_form'),
]
