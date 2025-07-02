from random import randint
from django.core.cache import cache
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status
from unicodedata import category
import pandas as pd
from .serializer import UserSerializer, LoginSerializer, ExpenseSerializer, RegisterSerializer
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from .tasks import email_verification_otp_mail, email_successfully_verified_mail
from rest_framework.throttling import UserRateThrottle
from uuid import uuid4
from .models import Expense
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse, HttpResponse

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
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views       import APIView
from rest_framework.response    import Response
from django.db.models           import Sum
from datetime                   import datetime
from dateutil.relativedelta     import relativedelta

from .models import Expense
from django.contrib.auth import get_user_model

User = get_user_model()

class UserExpenseSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # --- 1. Read filters ---
        user_id    = request.query_params.get("user_id")
        start_date = request.query_params.get("start_date")
        end_date   = request.query_params.get("end_date")
        month      = request.query_params.get("month")     # YYYY-MM
        category   = request.query_params.get("category")

        # --- 2. Build base user queryset ---
        if user_id:
            users = User.objects.filter(id=user_id)
        else:
            users = User.objects.all()

        result = []

        for user in users:
            # --- 3. Build filtered Expense queryset for this user ---
            qs = Expense.objects.filter(user=user)

            if start_date and end_date:
                qs = qs.filter(date__range=[start_date, end_date])
            elif month and category:
                try:
                    dt = datetime.strptime(month, "%Y-%m")
                    qs = qs.filter(
                        date__year = dt.year,
                        date__month = dt.month,
                        category   = category
                    )
                except ValueError:
                    return Response(
                        {"error": "Invalid month format. Use YYYY-MM."},
                        status=400
                    )
            elif month:
                try:
                    dt = datetime.strptime(month, "%Y-%m")
                    qs = qs.filter(
                        date__year  = dt.year,
                        date__month = dt.month
                    )
                except ValueError:
                    return Response(
                        {"error": "Invalid month format. Use YYYY-MM."},
                        status=400
                    )
            elif category:
                qs = qs.filter(category=category)

            # --- 4. Aggregate total spent ---
            total_spent = qs.aggregate(total=Sum("amount"))["total"] or 0

            # --- 5. Category‐wise breakdown ---
            cat_summary = (
                qs
                .values("category")
                .annotate(total=Sum("amount"))
                .order_by("category")
            )
            # Convert to list of simple dicts
            cat_list = [
                {"category": entry["category"], "total": entry["total"]}
                for entry in cat_summary
            ]

            result.append({
                "id":                user.id,
                "username":          user.username,
                "email":             user.email,
                "total_spent":       total_spent,
                "category_summary":  cat_list,
            })

        return Response(result)



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


# views.py

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"status": False, "error": serializer.errors}, status=400)

        validated_data = serializer.validated_data
        user = authenticate(username=validated_data['username'], password=validated_data['password'])

        if user is None:
            return Response({"status": False, "message": "Invalid Credentials"}, status=401)

        login(request, user)

        return Response({
            "status": 200,
            "message": "Login Successful",
            "is_staff": user.is_staff,  # ✅ return this
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



from rest_framework.views       import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response    import Response
from django.http                import HttpResponse
from django.db.models           import Sum
import pandas as pd

from .models import Expense

class ExportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data       = request.data
        user_id    = data.get("user_id")
        start_date = data.get("start_date")
        end_date   = data.get("end_date")
        category   = data.get("category")


        if request.user.is_staff and user_id:
            qs = Expense.objects.filter(user_id=user_id)
        else:
            qs = Expense.objects.filter(user=request.user)


        if start_date and end_date:
            qs = qs.filter(date__range=[start_date, end_date])


        if category:
            qs = qs.filter(category=category)


        if not qs.exists():
            return Response(
                {"error": "No data found for these filters."},
                status=404
            )

        df = pd.DataFrame(
            qs.values("id", "category", "date", "description","amount","user")
        )
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="expenses.xlsx"'

        with pd.ExcelWriter(response, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Expenses", index=False)

        return response

class CategoryListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Expense.objects.filter(user=request.user).values_list('category', flat=True).distinct()
        return Response({"categories": list(categories)})

class AllCategoriesAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        cats = Expense.objects.values_list("category", flat=True).distinct()
        return Response({"categories": list(cats)})

