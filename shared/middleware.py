from django.contrib.auth.models import User
from datetime import datetime

def lastActiveMiddleware(get_response):
    def middleware(request):
