from django.contrib.auth.models import User
from datetime import datetime

# THIS NEXT FUNCTION AND ITS CONTENTS WERE CREATED TO IMPLEMENT AN IDEA FROM
# CITATION [29]
def lastActiveMiddleware(get_response):
    def middleware(request):
        if request.user.is_authenticated and not request.user.is_staff:
            request.user.userinfo.lastActive = datetime.now()
            request.user.userinfo.save()
        return get_response(request)

    return middleware
