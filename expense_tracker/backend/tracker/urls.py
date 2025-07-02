from django.urls import path
from rest_framework import routers
from .views import RegisterAPIView, VerifyOTPView, LoginAPIView, LogoutAPIView, ExpenseAPIView, ExpenseDetailAPIView, \
    RegisterTemplateView, ExpenseStatsAPIView, ExpenseChartAPIView, ExpenseYearlyChartAPIView
from django.urls import path
from .views import get_csrf_token


urlpatterns = [
    path(
        "api/register/",
        RegisterAPIView.as_view()),
    path(
        "api/verify_otp/",
        VerifyOTPView.as_view()),
    path(
        "api/login/",
        LoginAPIView.as_view()),
    path(
        "api/logout/",
        LogoutAPIView.as_view()),
    path(
        'api/expenses/',
        ExpenseAPIView.as_view()),
    path(
        'api/expenses/<int:pk>/',
        ExpenseDetailAPIView.as_view(),
        name='expense-detail'),
    path(
        'api/csrf/',
        get_csrf_token),
    path(
        'register/',
        RegisterTemplateView.as_view()),
    path(
        'api/expenses/stats/',
        ExpenseStatsAPIView.as_view(),
        name='expense-stats'),
    path('api/expenses/chart/',
         ExpenseChartAPIView.as_view(),
         name='expense-chart'),
    path('api/expenses/yearly-chart/', ExpenseYearlyChartAPIView.as_view())
]
