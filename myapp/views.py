from django.shortcuts import render, redirect
from django.http import JsonResponse
from .tasks import send_otp_email
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

def send_otp(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'error': 'Email is required'}, status=400)

    send_otp_email.delay(email)
    return render(request, 'myapp/send_otp.html')

def home(request):
    return render(request, 'myapp/home.html')

def set_task_time(request):
    if request.method == 'POST':
        interval_minutes = request.POST.get('interval_minutes')
        if not interval_minutes:
            return JsonResponse({'error': 'Interval minutes is required'}, status=400)
        try:
            interval_minutes = int(interval_minutes)
            if interval_minutes <= 0:
                return JsonResponse({'error': 'Interval must be positive'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid interval value'}, status=400)

        # Create or get interval schedule
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=interval_minutes,
            period=IntervalSchedule.MINUTES,
        )

        # Create or update periodic task
        task_name = 'myapp.tasks.send_otp_email'
        periodic_task, created = PeriodicTask.objects.get_or_create(
            name='Send OTP Email Periodic Task',
            defaults={
                'interval': schedule,
                'task': task_name,
                'args': json.dumps(['example@example.com']),  # default arg, can be changed
            }
        )
        if not created:
            periodic_task.interval = schedule
            periodic_task.save()

        return JsonResponse({'message': f'Task interval set to {interval_minutes} minutes'})

    return JsonResponse({'error': 'Invalid request method'}, status=405)
