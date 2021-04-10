from .models import *
from background_task import background
import time

@background(schedule=5)
def process(task_id):
    for i in range(30):
        print(i)
        time.sleep(1)
    obj = Submission.objects.get(submission_id = task_id)
    obj.status = True
    obj.save()

