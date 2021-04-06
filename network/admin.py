from django.contrib import admin

# Register your models here.
from .models import UserUser, Like, Post

admin.site.register(UserUser)
admin.site.register(Like)
admin.site.register(Post)