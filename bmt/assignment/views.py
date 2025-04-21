from django.http import JsonResponse, HttpResponse

from .models import Assignment
from .tasks import my_task, send_assignment_email
from django.shortcuts import get_object_or_404



def trigger_my_task(request):
    arg1 = int(request.GET.get('arg1', 0))
    arg2 = int(request.GET.get('arg2', 0))

    # Call the task asynchronously
    task = my_task.delay(arg1, arg2)

    return JsonResponse({'task_id': task.id, 'status': 'Task submitted'})
def trigger_my_task3(request):
    return HttpResponse("The task was called successfully!")


# email

def notify_assignee_view(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    user_email = assignment.assigned_to.email
    send_assignment_email(user_email, assignment.title)

    return JsonResponse({'status': f'Email sent to {user_email}'})
