from celery import Celery
from . import celeryconfig


# Configure Celery
app = Celery('tasks')
app.config_from_object(celeryconfig)


# Define a Celery task
@app.task
def add(x, y):
    result = x + y
    return result
