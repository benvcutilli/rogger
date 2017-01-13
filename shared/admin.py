from django.contrib import admin
from shared.models import UserInfo, Follow, Block

# Register your models here.
admin.site.register(UserInfo)
admin.site.register(Follow)
admin.site.register(Block)
