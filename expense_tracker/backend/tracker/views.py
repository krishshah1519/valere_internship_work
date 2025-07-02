from random import randint
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from .serializer import UserSerializer, LoginSerializer, ExpenseSerializer, RegisterSerializer
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from .tasks import email_verification_otp_mail, email_successfully_verified_mail
from rest_framework.throttling import UserRateThrottle
from uuid import uuid4
from .models import Expense
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse

from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView

from rest_framework.response import Response
from django.db.models.functions import ExtractMonth
from django.db.models import Sum
from datetime import datetime
import calendar

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})


User = get_user_model()


class ExpenseYearlyChartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        year_str = request.GET.get('year')

        try:
            year = int(year_str) if year_str else datetime.now().year
        except ValueError:
            return Response({"error": "Invalid year format"}, status=400)

        expenses = Expense.objects.filter(user=user, date__year=year)
        monthly_summary = (
            expenses
            .annotate(month_num=ExtractMonth('date'))
            .values('month_num')
            .annotate(total=Sum('amount'))
            .order_by('month_num')
        )

        data = [
            {"month": calendar.month_abbr[entry['month_num']], "total": entry['total']}
            for entry in monthly_summary
        ]

        return Response({"monthly_summary": data})

class ExpenseStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        cache_key = f"expense_stats_{user.id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)

        today_total = Expense.objects.filter(
            user=user, date=today).aggregate(
            total=Sum('amount'))['total'] or 0
        week_total = Expense.objects.filter(
            user=user, date__gte=start_of_week).aggregate(
            total=Sum('amount'))['total'] or 0
        month_total = Expense.objects.filter(
            user=user, date__gte=start_of_month).aggregate(
            total=Sum('amount'))['total'] or 0

        data = {
            "today": today_total,
            "week": week_total,
            "month": month_total
        }

        cache.set(cache_key, data, timeout=600)

        return Response(data)


class OTPThrottle(UserRateThrottle):
    rate = "5/hour"





class ExpenseChartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        month_str = request.GET.get('month')

        try:
            month_date = datetime.strptime(month_str, "%Y-%m") if month_str else datetime.now()
        except ValueError:
            return Response({"error": "Invalid month format. Use YYYY-MM"}, status=400)

        start_of_month = month_date.replace(day=1)
        end_of_month = (start_of_month + relativedelta(months=1)) - timedelta(days=1)

        expenses = Expense.objects.filter(user=user, date__range=(start_of_month, end_of_month))
        category_data = expenses.values('category').annotate(total=Sum('amount'))
        date_data = expenses.values('date').annotate(total=Sum('amount')).order_by('date')

        chart_data = {
            "category_summary": list(category_data),
            "daily_summary": list(date_data)
        }

        return Response(chart_data)


class RegisterAPIView(APIView):
    throttle_classes = [OTPThrottle]
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data

        serializer = UserSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                "error": serializer.errors
            })

        validated_data = serializer.validated_data
        otp = generate_otp()

        token = AccessToken()
        token.set_exp(lifetime=timedelta(minutes=10))

        key_id = uuid4()
        token['key'] = str(key_id)

        cache.set(f"{str(key_id)}", {
            "username": validated_data['username'],
            "password": validated_data['password'],
            "email": validated_data['email'],
            "first_name": validated_data["first_name"],
            "last_name": validated_data["last_name"],
            "dob": str(validated_data["dob"]),
            "gender": validated_data["gender"],
            "phone_number": validated_data["phone_number"],
            "otp": str(otp)
        }, timeout=600)

        email_verification_otp_mail.delay(
            otp, validated_data['first_name'], validated_data['email'])

        return Response({
            "status": True,
            'message': 'OTP sent to your email. Please verify.',
            'otp_token': str(token)
        }, status=200)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('otp_token')
        input_otp = request.data.get('otp')

        try:
            token = AccessToken(token)
            key_id = token['key']
            cache_key = f"{str(key_id)}"
            user_data = cache.get(cache_key)

            if not user_data:
                return Response(
                    {"message": "Token expired or invalid."}, status=400)

            if str(user_data['otp']) != str(input_otp):
                return Response(
                    {"message": "Incorrect OTP."}, status=400)

            user_data.pop('otp')

            serializer = RegisterSerializer(data=user_data)
            if not serializer.is_valid():
                return Response(
                    {"error": serializer.errors}, status=400)
            serializer.save()

            email_successfully_verified_mail.delay(
                user_data['username'], user_data['email'])
            cache.delete(cache_key)
            return Response(
                {"message": "Account created successfully!"}, status=201)

        except Exception as e:
            return Response({
                "status": False,
                "message": "Invalid or Expired Token",
                "error": str(e)}, status=400
            )


class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": False,
                             "error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data

        user = authenticate(
            username=validated_data['username'],
            password=validated_data['password'])

        if user is None:
            return Response({"status": False,
                             "message": "Invalid Credentials"},
                            status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response({
            "status": 200,
            "message": "Login Successful."
        })


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"status": True,
                         "message": "Logout successful."},
                        status.HTTP_200_OK)


def generate_otp():
    return randint(100000, 999999)


class RegisterTemplateView(View):
    def get(self, request):
        return render(request, "tracker/templates/tracker/signup.html")


class ExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        date = request.GET.get('date')
        category = request.GET.get('category')

        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                return Response({"error": "Invalid date format"}, status=400)

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            expenses = expenses.filter(date__range=[start_date, end_date])

        if date:
            expenses = expenses.filter(date=date)
        if category:
            expenses = expenses.filter(category=category)
        serializer = ExpenseSerializer(expenses, many=True)

        return Response({
            "message": "Expenses successfully fetched",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        expenses = request.data
        serializer = ExpenseSerializer(data=expenses)
        if not serializer.is_valid():
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        serializer.save(user=request.user)
        cache.delete(f"expense_stats_{request.user.id}")

        return Response({"message": "Expense successfully added"},
                        status=status.HTTP_201_CREATED)


class ExpenseDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk, user=request.user)
        expense.delete()
        cache.delete(f"expense_stats_{request.user.id}")

        return Response({"message": "Expense deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        expense = get_object_or_404(Expense, pk=pk, user=request.user)
        serializer = ExpenseSerializer(
            expense, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        cache.delete(f"expense_stats_{request.user.id}")

        return Response("Expense successfully updated", status.HTTP_200_OK)
