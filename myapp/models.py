from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Issue_Model(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=240, null=True)
    issue_type = models.IntegerField()
    date_created = models.DateField(auto_now_add=True)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_user')
    affected_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='affected_user')
    is_solved = models.BooleanField(null=True) # 0 for unsolved, 1 for solved

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, max_length=500, blank=True)
    location = models.CharField(null=True, max_length=200)
    user_type = models.BooleanField(null=True) # 0 for user, 1 for ODITer
    birth_date = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
