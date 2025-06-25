from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from random import randint
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from ecommerce.settings import EMAIL_HOST_USER
from .forms import SignUp, ChangePasswordForm
from .models import Customer


def send_email(subject, email, otp, uname, html_content, text_content):

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()


def send_email_successful_verification(email):
    subject = "Email Successfully Verified"
    msg = "Your email has been successfully verified."
    sender_email = EMAIL_HOST_USER
    send_mail(subject, msg, sender_email, [email])


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
                subject = "Email Verification and Account Activation"
                context = {'user': data['username'], 'otp': otp}
                html_content = render_to_string(
                    'emails/otp_verification_mail.html', context)
                text_content = f"Hi {
                    data['username']},\nYour OTP is: {otp}. It is valid for 10 minutes.\nPlease do not share this code."
                send_email(
                    subject,
                    data['email'],
                    otp,
                    data['username'],
                    html_content,
                    text_content)
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

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid Username or Password.")
            return redirect('login')

    return render(request, 'ecommerce_website/login.html')


def index(request):
    return render(request, 'ecommerce_website/index.html')


def verify_otp(request):
    if request.method == "POST":
        user_input_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        user_data = request.session.get('pending_user')

        if user_input_otp and session_otp and int(
                user_input_otp) == int(session_otp):
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
            request.session.pop("pending_user", None)
            request.session.pop("otp", None)

            subject = "Account verified Successfully"
            context = {'user': user_data['username']}
            html_content = render_to_string(
                'emails/email-successfully_verified_mail.html', context)
            text_content = f"Hi {
                user_data['username']},\nYour email has been Successfully Verified.\nIf this is not you, please report via mail."
            send_email(
                subject,
                user_data['email'],
                None,
                user_data['username'],
                html_content,
                text_content)

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
        subject = "Account password change request "
        context = {'user': request.user.username, 'otp': otp}
        html_content = render_to_string(
            'emails/otp_verification_password_change_mail.html', context)
        text_content = f"Hi {
            request.user.username},\nYour OTP is: {otp}. It is valid for 10 minutes.\nPlease do not share this code."
        send_email(
            subject,
            request.user.email,
            otp,
            request.user.username,
            html_content,
            text_content)
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
    return


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

            subject = "Account password change successfully "
            context = {'user': request.user.username}
            html_content = render_to_string(
                'emails/password_successfully_changed_mail.html', context)
            text_content = f"Hi {
                request.user.username},\nYour Password has been successfully updated \nIf this is not you please report it ."
            send_email(
                subject,
                request.user.email,
                None,
                request.user.username,
                html_content,
                text_content)

            messages.success(
                request, "Your password was successfully changed!")
            return redirect('home')
    else:
        form = ChangePasswordForm(user=request.user)

    return render(request,
                  'ecommerce_website/change_password.html',
                  {'form': form})
