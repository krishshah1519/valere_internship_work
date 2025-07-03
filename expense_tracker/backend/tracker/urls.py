
from .views import RegisterAPIView, VerifyOTPView, LoginAPIView, LogoutAPIView, ExpenseAPIView, ExpenseDetailAPIView, \
     ExpenseChartAPIView, ExpenseYearlyChartAPIView, ExportAPIView, \
    CategoryListAPIView, UserExpenseSummaryAPIView, AllCategoriesAPIView
from django.urls import path
from .views import get_csrf_token


urlpatterns = [
    path("api/register/", RegisterAPIView.as_view()),
    path("api/verify_otp/", VerifyOTPView.as_view()),
    path("api/login/", LoginAPIView.as_view()),
    path("api/logout/", LogoutAPIView.as_view()),
    path('api/expenses/', ExpenseAPIView.as_view()),
    path('api/expenses/<int:pk>/', ExpenseDetailAPIView.as_view(), name= 'expense-detail'),
    path('api/csrf/',get_csrf_token),

    path('api/expenses/chart/',ExpenseChartAPIView.as_view(), name='expense-chart'),
    path('api/expenses/yearly-chart/', ExpenseYearlyChartAPIView.as_view()),
    path("api/export/", ExportAPIView.as_view()),
    path('api/categories/', CategoryListAPIView.as_view(), name='category-list'),
    path("api/admin/summary/", UserExpenseSummaryAPIView.as_view(), name="admin-summary"),
    path("api/admin/categories/", AllCategoriesAPIView.as_view(), name="admin-categories"),
]
