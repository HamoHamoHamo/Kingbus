from django.contrib import admin
from community.models import Profile, Post, Image, Comment, Recomment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Recomment)