from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from assignment.models import Assignment
from assignment.tasks import send_assignment_email

def assignment_email(instance, is_update=False, old_instance=None):
    user = instance.assigned_to

    context = {
        'assigned_to_name': user.username,
        'assignment_title': instance.title,
        'assignment_description': instance.description,
        'business_name': instance.business.name if instance.business else "N/A",
        'due_date': instance.due_date.strftime("%B %d, %Y") if instance.due_date else "N/A",
        'status': instance.status,
        'status_class': instance.status.lower().replace(' ', '-') if instance.status else "",
        'notes': instance.notes or "No additional notes.",
    }

    if is_update:
        context.update({
            'updated_by_name': instance.uploaded_by.username if instance.uploaded_by else "Admin",
            'title_changed': old_instance.title != instance.title,
            'previous_title': old_instance.title if old_instance.title != instance.title else None,
            'due_date_changed': old_instance.due_date != instance.due_date,
            'previous_due_date': old_instance.due_date.strftime("%B %d, %Y") if old_instance.due_date != instance.due_date else None,
            'status_changed': old_instance.status != instance.status,
            'previous_status': old_instance.status if old_instance.status != instance.status else None,
        })
    else:
        context['uploaded_by_name'] = instance.uploaded_by.username if instance.uploaded_by else "Admin"

    return context

@receiver(pre_save, sender=Assignment)
def notify_user_on_assignment_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = Assignment.objects.get(pk=instance.pk)
    except Assignment.DoesNotExist:
        return

    if not instance.assigned_to:
        return

    context = assignment_email(instance, is_update=True, old_instance=old_instance)
    subject = f"Assignment Updated: {instance.title}"
    template_name = 'changed_email.html'
    send_assignment_email.delay(instance.assigned_to.email, subject, context, template_name)


@receiver(post_save, sender=Assignment)
def notify_user_on_assignment_creation(sender, instance, created, **kwargs):
    if not created or not instance.assigned_to:
        return

    context = assignment_email(instance, is_update=False)
    subject = f"New Assignment: {instance.title}"
    template_name = 'email.html'
    send_assignment_email.delay(instance.assigned_to.email, subject, context, template_name)
