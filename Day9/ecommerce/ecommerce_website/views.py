from django.shortcuts import render, redirect
from django.core.mail import send_mail
from ecommerce_site.settings import EMAIL_HOST_USER


from .models import Customer
import uuid
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

# Create your views here.


def generate_random_alphanumeric(length):
    """Generates a random alphanumeric string of the specified length."""
    return get_random_string(length)


def send_email(email, otp):
    subject = "Email Verification and Account Activation"
    msg = f"This is your OTP:\033 {otp} \033 for verifying your email."
    sender_email = EMAIL_HOST_USER
    send_mail(subject, msg, sender_email, [email])


def send_email1(email):
    subject = "Email Verification and Account Activation"
    msg = f"Email has been Successfully verified"
    sender_email = EMAIL_HOST_USER
    send_mail(subject, msg, sender_email, [email])


@login_required
def index(request):
    return render(request, 'ecommerce_website/index.html')


def home(request):
    return render(request, "ecommerce_website/home.html")


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            Customer.objects.get(email=email, password=password)
            return home(request)
        except Customer.DoesNotExist:
            return render(request, "ecommerce_website/login.html",
                          {"error_message": "Invalid email or password."})
    return render(request, "ecommerce_website/login.html")

#
# def signup(request):
#     if request.method == "POST":
#         name = request.POST["name"]
#         dob = request.POST["dob"]
#         gender = request.POST["gender"]
#         phone = request.POST["phone"]
#         email = request.POST["email"]
#         password = request.POST["password"]
#
#         # Prevent duplicate emails
#         if Customer.objects.filter(email=email).exists():
#             return render(
#                 request, "signup.html", {
#                     "error_message": "Email already registered."})
#
#         send_email(email)
#
#         # Save new customer
#         Customer.objects.create(
#             customer_id=uuid.uuid4(),
#             name=name,
#             DOB=dob,
#             gender=gender,
#             phone_number=phone,
#             email=email,
#             password=password  # 🔒 Consider hashing in production!
#
#         )
#
#         return redirect("login")
#
#     return render(request, "ecommerce_website/signup.html")
#


def signup(request):
    if request.method == "POST":
        name = request.POST["name"]
        dob = request.POST["dob"]
        gender = request.POST["gender"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["password"]

        if Customer.objects.filter(email=email).exists():
            return render(request, "ecommerce_website/signup.html", {
                "error_message": "Email already registered."
            })

        otp = generate_random_alphanumeric(6)
        send_email(email, otp)

        request.session['pending_user'] = {
            "name": name,
            "dob": dob,
            "gender": gender,
            "phone": phone,
            "email": email,
            "password": password,
        }
        request.session['otp'] = otp

        return redirect('verify_otp')

    return render(request, "ecommerce_website/signup.html")


def verify_otp(request):
    if request.method == "POST":
        user_input_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        user_data = request.session.get("pending_user")

        if user_input_otp == session_otp and user_data:
            Customer.objects.create(
                customer_id=uuid.uuid4(),
                name=user_data["name"],
                DOB=user_data["dob"],
                gender=user_data["gender"],
                phone_number=user_data["phone"],
                email=user_data["email"],
                password=user_data["password"],
                is_verified=True
            )

            request.session.pop("pending_user", None)
            request.session.pop("otp", None)
            send_email1(user_data['email'])
            return redirect("login")
        else:
            return render(request, "ecommerce_website/verify_otp.html", {
                "error_message": "Invalid OTP. Please try again."
            })

    return render(request, "ecommerce_website/verify_otp.html")
