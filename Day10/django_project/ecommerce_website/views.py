from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.auth import logout
from random import randint

from Demos.win32ts_logoff_disconnected import username
from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from ecommerce.settings import EMAIL_HOST_USER
from .forms import SignUp
from .models import Customer
from django.contrib.auth import authenticate, login as auth_login


# Create your views here.

def send_email(email, otp, uname):
    subject = "Email Verification and Account Activation"
    from_email = EMAIL_HOST_USER
    to_email = [email]
    name = uname

    # Context to pass to the HTML template
    context = {
        'user': name,
        'otp': otp
    }

    # Render HTML email from template
    html_content = render_to_string('emails/emails.html', context)

    # Optional: plain text version
    text_content = f"Hi {uname},\nYour OTP is: {otp}. It is valid for 5 minutes.\nPlease do not share this code."

    # Send the email
    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()


def send_email1(email):
    subject = "Email Verification and Account Activation"
    msg = f"Email has been Successfully verified"
    sender_email = EMAIL_HOST_USER
    send_mail(subject, msg, sender_email, [email])


def generate_otp():
    return randint(100000, 999999)


@login_required()
def home(request):
    return render(request, 'ecommerce_website/home.html')


def signup(request):
    form = SignUp()
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        phone_number = request.POST["phone_number"]

        if Customer.objects.filter(email=email).exists():
            return render(request, "ecommerce_website/signup.html", {
                "error_message": "Email already registered.",
                'form': form
            })
        if Customer.objects.filter(username=username).exists():
            return render(request, "ecommerce_website/signup.html", {
                "error_message": "Username already registered.",
                'form': form
            })
        form = SignUp(request.POST)
        if form.is_valid():
            authenticate()
            otp = generate_otp()
            send_email(email, otp, username)
            request.session['pending_user'] = {
                "username": username,
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "dob": dob,
                "gender": gender,
                "phone_number": phone_number,
            }
            print(otp)
            request.session['otp'] = otp
            return redirect('verify_otp')

    return render(request, 'ecommerce_website/signup.html', {'form': form})


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            return home(request)
        else:
            return redirect(
                '/login/', {"error_message": "Invalid Username or Password, Please try again"})
    else:
        return render(request, 'ecommerce_website/login.html')


def index(request):
    return render(request, 'ecommerce_website/index.html')


def verify_otp(request):
    if request.method == "POST":
        user_input_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        user_data = request.session.get('pending_user')

        if int(user_input_otp) == int(session_otp) and user_data:
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
            send_email1(user_data['email'])
            return redirect("login")
        else:
            return redirect("ecommerce_website/verify_otp.html", {
                "error_message": "Invalid OTP. Please try again."
            })
    return render(request, "ecommerce_website/verify_otp.html")


def log_out(request):
    logout(request)
    return redirect('login')


def change_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        try:
            user = Customer.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={
                        'uidb64': uid, 'token': token})
            )

            subject = "Reset Your Password"
            message = f"Hi {
                user.username},\nClick the link below to reset your password:\n{reset_link}\n\nIf you did not request this, ignore this email."
            from_email = EMAIL_HOST_USER
            to_email = [email]

            send_mail(subject, message, from_email, to_email)

            return render(request, 'ecommerce_website/change_password.html', {
                'success_message': "Password reset link has been sent to your email."
            })

        except Customer.DoesNotExist:
            return render(request, 'ecommerce_website/change_password.html', {
                'error_message': "No account found with this email."
            })

    return render(request, 'ecommerce_website/change_password.html')
