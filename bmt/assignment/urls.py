from django.urls import path
from . import views
from .views import notify_assignee_view

urlpatterns = [
    path('run-task/', views.trigger_my_task, name='trigger_my_task'),
    path('run-task3/', views.trigger_my_task3, name='trigger_my_task3'),
    #path('send-email/', send_email_view, name='send_email'),

    path('notify/<int:assignment_id>/', notify_assignee_view, name='notify_assignee'),
]
