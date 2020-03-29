from django.db import models

# Create your models here.
class Issue_Model(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=240, null=True)
    issue_type = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    assigned_user = models.CharField(max_length=50, null=True)
    affected_user = models.CharField(max_length=50, null=True)
    is_solved = models.BooleanField(null=True) # 0 for unsolved, 1 for solved

class User_Model(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    user_type = models.BooleanField() # 0 for user, 1 for ODITer
    username = models.CharField(max_length=50)