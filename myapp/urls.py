from django.urls import path
from .views import send_otp, home, set_task_time

urlpatterns = [
    path('', home),
    path('send-otp/', send_otp),
    path('set-task-time/', set_task_time, name='set_task_time'),
]
