from django.db import models
from django.contrib.auth.models import User
import boto3
from rogger.settings import MEDIA_BUCKET_NAME, MEDIA_BUCKET_ID, MEDIA_BUCKET_SECRET, PROFILE_PICTURE_EXPIRATION_SECONDS, DEFAULT_PROFILE_PICTURE_FILENAME, STATIC_URL

# Create your models here.

class UserInfo(models.Model):
    # next line from citation [14]
    authUser                =   models.OneToOneField(User, on_delete=models.CASCADE)
    displayName             =   models.CharField(max_length=100, default="")
    privacySelection        =   models.IntegerField(default=1)
    pdfName                 =   models.CharField(max_length=100, default="")
    # NEXT LINE CITATION [27]
    uploadedProfilePicture  =   models.BooleanField(default=False)

    def profilePictureURL(self):
        if self.uploadedProfilePicture:
            s3client = boto3.client('s3', aws_secret_access_key=MEDIA_BUCKET_SECRET, aws_access_key_id=MEDIA_BUCKET_ID)
            # SENDING A PRESIGNED URL FROM [28]
            return s3client.generate_presigned_url(
                                                    'get_object',
                                                    Params={ Bucket=MEDIA_BUCKET_NAME, Key=("profilepictureofuser" + str(self.authUser.id) + ".jpg") },
                                                    ExpiresIn=PROFILE_PICTURE_EXPIRATION_SECONDS
            )
        else:
            return STATIC_URL + DEFAULT_PROFILE_PICTURE_FILENAME

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
