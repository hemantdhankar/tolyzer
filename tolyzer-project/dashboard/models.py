from django.db import models
import uuid
# Create your models here.

class Submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    uploaded_file = models.FileField(upload_to='upload/')
    status = models.BooleanField(default = False)
    
    
class Result(models.Model):
    submission_id = models.ForeignKey(Submission,on_delete=models.CASCADE)
    rating = models.CharField(max_length=5)
    crucial_nodes = models.CharField(max_length=100)
    graph1 = models.ImageField(upload_to='results/', height_field=None, width_field=None, max_length=100)
    graph2 = models.ImageField(upload_to='results/', height_field=None, width_field=None, max_length=100)
    graph3 = models.ImageField(upload_to='results/', height_field=None, width_field=None, max_length=100)
