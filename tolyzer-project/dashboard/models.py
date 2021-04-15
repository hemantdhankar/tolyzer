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
    diameter = models.FloatField(null=True)
    edges = models.FloatField(null=True)
    nodes = models.FloatField(null=True)
    density = models.FloatField(null=True)
    cpl = models.FloatField(null=True)
    average_degree = models.FloatField(null=True)
    top_5_degree_nodes = models.TextField(null=True)
    top_5_bc_nodes = models.TextField(null=True)
    failure_tolerance = models.TextField(null=True)
    attack_tolerance = models.TextField(null=True)
    recommended_file = models.FileField(null=True)
    
    graph1 = models.ImageField(upload_to='results/', height_field=None, width_field=None, max_length=100)
    graph2 = models.ImageField(upload_to='results/', height_field=None, width_field=None, max_length=100)
    graph3 = models.ImageField(upload_to='results/', height_field=None, width_field=None, max_length=100)
