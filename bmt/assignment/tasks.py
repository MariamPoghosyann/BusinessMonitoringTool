# from celery import shared_task
# import smtplib, ssl
# import os
#
# @shared_task
# def send_assignment_email(receiver_email, subject, body):
#     sender_email = "tinn.marutyan.04@gmail.com"
#     password = "your real password here"  # use an env var!
#
#     message = f"Subject: {subject}\n\n{body}"
#     context = ssl._create_unverified_context()
#
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#         server.login(sender_email, password)
#         server.sendmail(sender_email, receiver_email, message)


from celery import shared_task
from django.http import HttpResponse


@shared_task(name='my_task')
def my_task(arg1, arg2):
    # Task logic here
    result = arg1 + arg2
    return result


@shared_task(name='my_task2')
def my_task2(arg1, arg2):
    result = arg1 - arg2
    return result

@shared_task(name='my_task3')
def my_task3(request):
    return HttpResponse("The task was called successfully!")

from django.core.mail import send_mail

from celery import shared_task
from django.core.mail import send_mail

@shared_task(name='send_assignment_email')
def send_assignment_email(to_email, subject, message):

    subject = f'New Assignment:'
    message = f'You have been assigned a new task: Please check your dashboard for details.'

    send_mail(
        subject,
        message,
        'poghosyanmariam44@gmail.com',
        [to_email],
        fail_silently=False,
    )
