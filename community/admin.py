from django.contrib import admin
from community.models import Community_profile, Post, Photo, Comment, Recomment
# Register your models here.

admin.site.register(Community_profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Recomment)