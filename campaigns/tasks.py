from celery import shared_task
import time

@shared_task
def test_worker():
    print("Celery Worker received the task...")
    time.sleep(3) # Simulate a time-consuming process like sending an email
    print("Task complete! Celery is fully operational.")
    return "SUCCESS"