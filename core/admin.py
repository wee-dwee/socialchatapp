from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(post)
admin.site.register(like_post)
admin.site.register(FollowersCount)