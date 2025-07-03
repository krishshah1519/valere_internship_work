from django.contrib.auth import get_user_model
from .models import Expense
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from expense_tracker.settings import EMAIL_HOST_USER
from django.core.mail import get_connection


@shared_task
def email_verification_otp_mail(otp, name, email):
    connection = get_connection()
    print(
        f"[TASK] email_verification_otp_mail called with otp={otp}, name={name}, email={email}")
    subject = "Email Verification and Account Activation"
    context = {'user': name, 'otp': otp}
    html_content = render_to_string(
        'emails/otp_verification_mail.html', context)
    text_content = f"Hi {name},\nYour OTP is: {otp}. It is valid for 10 minutes.\nPlease do not share this code."
    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email, connection=connection)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
    connection.close()


@shared_task
def email_successfully_verified_mail(name, email):
    connection = get_connection()
    subject = "Account verified Successfully"
    context = {'user': {name}}
    html_content = render_to_string(
        'emails/email_successfully_verified_mail.html', context)
    text_content = f"Hi {name},\nYour email has been Successfully Verified.\nIf this is not you, please report via mail."

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email, connection=connection)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
    connection.close()


@shared_task
def password_change_otp_mail(otp, name, email):
    connection = get_connection()
    subject = "Account password change request "
    context = {'user': name, 'otp': otp}
    html_content = render_to_string(
        'emails/otp_verification_for_password_change_mail.html',
        context)
    text_content = f"Hi {name},\nYour OTP is: {otp}. It is valid for 10 minutes.\nPlease do not share this code."

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email, connection=connection)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
    connection.close()


@shared_task
def password_changed_successfully_mail(name, email):
    connection = get_connection()
    subject = "Account password change successfully "
    context = {'user': name}
    html_content = render_to_string(
        'emails/password_successfully_changed_mail.html', context)
    text_content = f"Hi {name},\nYour Password has been successfully updated \nIf this is not you please report it ."

    from_email = EMAIL_HOST_USER
    to_email = [email]

    email_message = EmailMultiAlternatives(
        subject, text_content, from_email, to_email, connection=connection)
    email_message.attach_alternative(html_content, "text/html")
    email_message.send()
    connection.close()


User = get_user_model()


@shared_task
def send_weekly_expense_summary():
    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    users = User.objects.all()
    for user in users:
        expenses = Expense.objects.filter(
            user=user, date__range=[last_week, today])
        if not expenses.exists():
            continue

        total = sum(exp.amount for exp in expenses)
        category_summary = {}
        for exp in expenses:
            category_summary.setdefault(exp.category, 0)
            category_summary[exp.category] += exp.amount

        message = render_to_string('emails/weekly_email_template.html', {
            'user': user,
            'total': total,
            'category_summary': category_summary,
            'start_date': last_week,
            'end_date': today,
        })

        send_mail(
            subject='Your Weekly Expense Summary',
            message='',
            from_email='noreply@yourapp.com',
            recipient_list=[user.email],
            html_message=message
        )
