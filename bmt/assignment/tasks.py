from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task(name='send_assignment_email')
def send_assignment_email(to_email, subject, context):
    html_content = render_to_string('email.html', context)

    # Generate plain text version by stripping the HTML
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

# @shared_task(name='my_task')
# def my_task(arg1, arg2):
#     # Task logic here
#     result = arg1 + arg2
#     return result
#
#
# @shared_task(name='my_task2')
# def my_task2(arg1, arg2):
#     result = arg1 - arg2
#     return result
#
# @shared_task(name='my_task3')
# def my_task3(request):
#     return HttpResponse("The task was called successfully!")