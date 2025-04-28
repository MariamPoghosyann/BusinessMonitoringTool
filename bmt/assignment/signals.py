from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment
from .tasks import send_assignment_email

@receiver(post_save, sender=Assignment)
def notify_user_on_assignment_change(sender, instance, created, **kwargs):
    if not instance.assigned_to:
        return  # No user assigned, no email needed

    user = instance.assigned_to

    context = {
        'assigned_to_name': user.username,
        'assignment_title': instance.title,
        'assignment_description': instance.description,
        'business_name': instance.business.name if instance.business else "N/A",
        'due_date': instance.due_date,
        'status': instance.status,
        'status_class': instance.status.lower().replace(' ', '-') if instance.status else "",
        'uploaded_by_name': instance.uploaded_by.username if instance.uploaded_by else "Admin",
        'notes': instance.notes if hasattr(instance, 'notes') and instance.notes else "No additional notes.",
    }

    if created:
        subject = f"New Assignment: {instance.title}"
    else:
        subject = f"Assignment Updated: {instance.title}"

    send_assignment_email.delay(user.email, subject, context)
