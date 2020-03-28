from django.db import models
from django.contrib.auth.models import User
import boto3
from rogger.settings import MEDIA_BUCKET_NAME, MEDIA_BUCKET_ID, MEDIA_BUCKET_SECRET, PROFILE_PICTURE_EXPIRATION_SECONDS, DEFAULT_PROFILE_PICTURE_FILENAME, STATIC_URL
import datetime
from django.utils import timezone
# USING AND IMPORTING botocore: CITATION [51]
import botocore

# A. This code comes up with an presigned URL [73] (URLs defined by [74]
#    according to [75, History]). I had originally thought that if the user had
#    set their profile privacy to "Completely hidden" (see
#    settings/settings.html) but that somehow a URL with bad authentication
#    failed and produced a 403 [76, 10.4.4] on the profile picture of the
#    "Completely hidden", that it would reveal that though the requester didn't
#    have the proper credentials, the user's profile picture exists, which
#    implies that the account exists (which is a security hole). However, [72,
#    Tim Gautier's answer] said that since the credentials don't work, the
#    requester may not even be able to find out the names of the objects in the
#    S3 bucket, so it would return a 403 for every request for an object to that
#    bucket. They mentioned this is a security feature explicitly made to combat
#    those bad actors trying to find out simply if an object exists. Since I am
#    looking for responses that do not reveal existence of an account, this
#    solves my problem. I tested this out with a modification of the code here
#    (actually, just a modification of the section of code commented by this
#    point in profilePictureURL(...) and the import statements at the top of
#    this file that looks like this:
#       from rogger.settings import MEDIA_BUCKET_NAME, MEDIA_BUCKET_ID, MEDIA_BUCKET_SECRET, PROFILE_PICTURE_EXPIRATION_SECONDS, DEFAULT_PROFILE_PICTURE_FILENAME, STATIC_URL
#       import boto3
#       import botocore
#       s3client = boto3.client(
#                                    's3',
#                                    aws_secret_access_key=MEDIA_BUCKET_SECRET,
#                                    aws_access_key_id=MEDIA_BUCKET_ID,
#                                    region_name="us-west-1",
#                                    config=botocore.config.Config(signature_version="s3v4")
#                   )
#       s3client.generate_presigned_url(
#                                                    'get_object',
#                                                    Params={
#                                                             'Bucket' : MEDIA_BUCKET_NAME,
#                                                             'Key' : "profilepictureofuser"+<user number>+".png"
#                                                    },
#                                                    ExpiresIn=10
#                   )
#    where <user number> is a Python string holding a User[81, "User"
#    documentation]'s model [82] "automatic primary key" [82, Automatic primary
#    key fields]) to generate (using the manage.py shell, on the Rogger server,
#    provided by Django [79, "shell" subcomand] invoked by the "python" command
#    provided by Python 3.5.2 [80]) a URL that refers to an S3 object key that
#    doesn't exist (I chose an automatic primary key that doesn't belong to any
#    user), and I got a 403 putting that URL into Firefox [78]. I also tried a
#    presigned URL generated with a real user's automatic primary key after the
#    time limit on said presigned URL expired, which also returned 403 response,
#    confirming the reasoning that 403s will appear for both objects requested
#    with invalid authentication supplied with the URL and URLs with bad
#    authentication credentials that point to objects that don't exist. Further,
#    the XML (according to [84, "Extensible Markup Language (XML)" right-side
#    box], [83] is the standard for XML) returned by both requests looked
#    essentially identical, meaning that there appeared to be no differences in
#    the XML that would suggest that S3 is leaking account-existence data.
#    "STATIC_URL" in the test code above is not related to this test; it was
#    just in the import line from the top of this file, so it was copied over
#    for the test, and refers to [85, "STATIC_URL" documentation] used in the
#    rogger/settings.py file which was set up probably by the
#      "django-admin startproject <project name>"
#    command from [79, "startproject" documentation].

class UserInfo(models.Model):
    # next line from citation [14]
    authUser                =   models.OneToOneField(User, on_delete=models.CASCADE)
    # NEXT LINE CITATION [31]
    displayName             =   models.CharField(max_length=100, default="")
    # 2 FOR DEFAULT: strong default privacy is mandated by GDPR [64] according
    # to [50], so we choose privacy setting 2, which is a protected profile;
    # however, according to [50], it may be necessary to have mode 3 by default
    # (unlisted profile) as it is technically the strongest privacy setting
    # Rogger has to offer.
    privacySelection        =   models.IntegerField(default=2)
    pdfName                 =   models.CharField(max_length=100, default="")
    # NEXT LINE CITATION [27]
    uploadedProfilePicture  =   models.BooleanField(default=False)
    searchUsername          =   models.BooleanField(default=True)
    searchDisplayName       =   models.BooleanField(default=True)
    # NEXT ATTRIBUTE FROM CITATION [29]
    lastActive              =   models.DateTimeField(default=timezone.now())

    def profilePictureURL(self):
        if self.uploadedProfilePicture:

            # Please read point A at the top of this file for a comment regarding this code.
            ################################################################################################################
            #                                                                                                              #

            # config PARAMETER VALUE: CITATION [51]
            s3client = boto3.client(
                                    's3',
                                    aws_secret_access_key=MEDIA_BUCKET_SECRET,
                                    aws_access_key_id=MEDIA_BUCKET_ID,
                                    region_name="us-west-1",
                                    config=botocore.config.Config(signature_version="s3v4")
            )
            # SENDING A PRESIGNED URL FROM CITATION [28]
            return s3client.generate_presigned_url(
                                                    'get_object',
                                                    Params={
                                                             'Bucket' : MEDIA_BUCKET_NAME,
                                                             'Key' : "profilepictureofuser"+str(self.authUser.id)+".png"
                                                    },
                                                    ExpiresIn=PROFILE_PICTURE_EXPIRATION_SECONDS
            )

            #                                                                                                              #
            ################################################################################################################

        else:
            return STATIC_URL + DEFAULT_PROFILE_PICTURE_FILENAME

    def thumbURL(self):
        if self.uploadedProfilePicture:

            # Please read point A at the top of this file for a comment regarding this code.
            ################################################################################################################
            #                                                                                                              #

            # config PARAMETER VALUE: CITATION [51]
            s3client = boto3.client(
                                    's3',
                                    aws_secret_access_key=MEDIA_BUCKET_SECRET,
                                    aws_access_key_id=MEDIA_BUCKET_ID,
                                    region_name="us-west-1",
                                    config=botocore.config.Config(signature_version="s3v4")
            )
            # SENDING A PRESIGNED URL FROM CITATION [28]
            return s3client.generate_presigned_url(
                                                    'get_object',
                                                    Params={
                                                             'Bucket' : MEDIA_BUCKET_NAME,
                                                             'Key' : "thumbofuser"+str(self.authUser.id)+".png"
                                                    },
                                                    ExpiresIn=PROFILE_PICTURE_EXPIRATION_SECONDS
            )

            #                                                                                                              #
            ################################################################################################################
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
