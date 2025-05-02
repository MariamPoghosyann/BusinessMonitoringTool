from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@shared_task(name='send_assignment_email')
def send_assignment_email(to_email, subject, context, template_name):
    html_content = render_to_string(template_name, context)

    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        to=[to_email],
    )

    email.attach_alternative(html_content, "text/html")
    email.send()

