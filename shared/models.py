from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserInfo(models.Model):
    # next line from citation [14]
    authUser            =   models.OneToOneField(User, on_delete=models.CASCADE)
    displayName         =   models.CharField(max_length=100, default="")
    privacySelection    =   models.IntegerField(default=1)
    pdfName             = models.CharField(max_length=100, default="")

class Follow(models.Model):
    # related_name usage in next line: citation [20]
    followee    =   models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followee_set")
    # related_name usage in next line: citation [20]
    follower    =   models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower_set")
    # "approved" attribute: citation [25]
    approved    =   models.BooleanField(default=False)

class Block(models.Model):
    # related_name usage in next line: citation [20]
    blockee     =   models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blockee_set")
    # related_name usage in next line: citation [20]
    blocker     =   models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_blocker_set")
