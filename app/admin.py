from django.contrib import admin

from app.models import Profile, Post, Comment, Bookmark

# Register your models here.


admin.site.register([Profile, Post, Comment, Bookmark])