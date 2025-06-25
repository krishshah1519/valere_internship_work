from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from random import randint
from django.shortcuts import render, redirect, reverse
from django.core.mail import  EmailMultiAlternatives
from django.contrib import messages
from ecommerce.settings import EMAIL_HOST_USER
from .forms import SignUp, ChangePasswordForm
from .models import Customer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.http.response import JsonResponse


class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})

def email_verification_otp_mail(otp,name,email):
    subject = "Email Verification and Account Activation"
    context = {'user':name, 'otp': otp}
    html_content = render_to_string(
        'emails/otp_verification_mail.html', context)
    text_content = f"Hi {name},\nYour OTP is: {otp}. It is valid for 10 minutes.\nPlease do not share this code."
    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

def email_successfully_verified_mail(name,email):
    subject = "Account verified Successfully"
    context = {'user': {name}}
    html_content = render_to_string(
        'emails/email_successfully_verified_mail.html', context)
    text_content = f"Hi {name},\nYour email has been Successfully Verified.\nIf this is not you, please report via mail."

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
def password_change_otp_mail(otp,name,email):
    subject = "Account password change request "
    context = {'user': name, 'otp': otp}
    html_content = render_to_string(
        'emails/otp_verification_for_password_change_mail.html', context)
    text_content = f"Hi {name},\nYour OTP is: {otp}. It is valid for 10 minutes.\nPlease do not share this code."

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

def password_changed_successfully_mail(name,email):

    subject = "Account password change successfully "
    context = {'user': name}
    html_content = render_to_string(
        'emails/password_successfully_changed_mail.html', context)
    text_content = f"Hi {name},\nYour Password has been successfully updated \nIf this is not you please report it ."

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()

def generate_otp():
    return randint(100000, 999999)


@login_required
def home(request):
    return render(request, 'ecommerce_website/home.html')


def signup(request):
    form = SignUp()
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if Customer.objects.filter(email=data['email']).exists():
                messages.error(request, "Email already registered.")
            elif Customer.objects.filter(username=data['username']).exists():
                messages.error(request, "Username already taken.")
            else:
                otp = generate_otp()
                email_verification_otp_mail(
                    otp,
                    data['username'],
                    data['email']
                )
                request.session['pending_user'] = {
                    "username": data['username'],
                    "email": data['email'],
                    "password": data['password1'],
                    "first_name": data['first_name'],
                    "last_name": data['last_name'],
                    "dob": str(data['dob']),
                    "gender": data['gender'],
                    "phone_number": data['phone_number'],
                }
                request.session['otp'] = otp
                return redirect('verify_otp')
    return render(request, 'ecommerce_website/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user :
            login(request, user)
            # token, created = Token.objects.get_or_create(user=user)
            # return JsonResponse({'token': token.key})
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password.")
            return redirect('login')

    return render(request, 'ecommerce_website/login.html')


def index(request):
    return render(request, 'ecommerce_website/index.html')


def create_customer(user_data):

    Customer.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
        dob=user_data["dob"],
        gender=user_data["gender"],
        phone_number=user_data["phone_number"],
    )
def verify_otp(request):
    if request.method == "POST":
        user_input_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        user_data = request.session.get('pending_user')

        if user_input_otp and session_otp and int(
                user_input_otp) == int(session_otp):
            create_customer(user_data)

            request.session.pop("pending_user", None)
            request.session.pop("otp", None)

            email_successfully_verified_mail(user_data['username'],user_data['email'])

            messages.success(
                request, "Account created successfully. Please login.")
            return redirect("login")

        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return render(request, "ecommerce_website/verify_otp.html")

    return render(request, "ecommerce_website/verify_otp.html")


@login_required
def log_out(request):
    logout(request)
    return redirect('login')


@login_required
def change_password(request):
    if request.method == "GET":
        otp = generate_otp()

        password_change_otp_mail(otp,request.user.username,request.user.email)
        request.session['password_change_otp'] = otp

        return render(
            request,
            'ecommerce_website/verify_change_password_otp.html')

    elif request.method == "POST":
        user_input_otp = request.POST.get("otp")
        session_otp = request.session.get("password_change_otp")

        if user_input_otp and session_otp and int(
                user_input_otp) == int(session_otp):
            request.session['otp_verified'] = True
            return redirect('change_password_form')
        else:
            messages.error(request, "Invalid OTP. Try again.")
            return render(
                request,
                'ecommerce_website/verify_change_password_otp.html')
    return reverse('home')


@login_required
def change_password_form(request):
    if not request.session.get('otp_verified'):
        return redirect('change_password')

    if request.method == 'POST':
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            request.session.pop('otp_verified', None)

            password_changed_successfully_mail(request.user.username, request.user.email)

            messages.success(
                request, "Your password was successfully changed!")
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request,
                  'ecommerce_website/change_password.html',
                  {'form': form})
