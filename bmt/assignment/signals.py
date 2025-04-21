from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment
from .tasks import send_assignment_email

@receiver(post_save, sender=Assignment)
def notify_user_on_assignment_create(sender, instance, created, **kwargs):
    if created:
        user = instance.assigned_to

        context = {
            'assigned_to_name': user.username,
            'assignment_title': instance.title,
            'assignment_description': instance.description,
            'business_name': instance.business.name,  # Optional: replace with dynamic business name
            'due_date': instance.due_date,
            'status': instance.status,
            'status_class': instance.status.lower().replace(' ', '-'),  # e.g., "In Progress" -> "in-progress"
            'uploaded_by_name': instance.uploaded_by.username if instance.uploaded_by else "Admin",
            'notes': instance.notes if hasattr(instance, 'notes') and instance.notes else "No additional notes.",
        }

        subject = f"New Assignment: {instance.title}"

        # Send the email via Celery
        send_assignment_email.delay(user.email, subject, context)

