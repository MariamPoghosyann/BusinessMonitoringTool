from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import Assignment
from .tasks import send_assignment_email

@receiver(post_save, sender=Assignment)
def notify_user_on_assignment_create(sender, instance, created, **kwargs):
    if created:
        def send_email_after_commit():
            user = instance.assigned_to
            subject = f"New Assignment: {instance.title}"
            message = (
                f"Hi {user.username},\n\n"
                f"You’ve been assigned a new task:\n\n"
                f"{instance.description}\n\n"
                f"Due: {instance.due_date}"
            )

            # Celery task
            send_assignment_email.delay(user.email, subject, message)

        transaction.on_commit(send_email_after_commit)

