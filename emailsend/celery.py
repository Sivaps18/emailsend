import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emailsend.settings")

app = Celery("emailsend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Use solo pool for Windows to avoid multiprocessing issues
app.conf.worker_pool = 'solo'
