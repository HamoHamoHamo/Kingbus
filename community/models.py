import os
from uuid import uuid4
from django.utils import timezone
from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=32,unique=True)

    scrap = models.ManyToManyField('Post', related_name='scrap', blank=True)
    blocked_profile = models.ManyToManyField('self', symmetrical=False, blank=True)
    liked_post = models.ManyToManyField('Post', related_name='liked_post', blank=True)
    liked_comment = models.ManyToManyField('Comment', related_name='liked_comment', blank=True)
    liked_recomment = models.ManyToManyField('Recomment', related_name='liked_recomment', blank=True)
    
    # def __str__(self) -> str:
    #     return self.nickname
    class Meta:
        db_table = 'kingbus_community_profile'


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    kinds = models.CharField(max_length=50)
    content = models.TextField()
    view = models.PositiveIntegerField(default=0)
    like_cnt = models.PositiveIntegerField(default=0) # 좋아요 수
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # def __str__(self) -> str:
    #     return self.title
    class Meta:
            db_table = 'kingbus_community_post'


class Image(models.Model):
    def upload_to_func(instance, filename):
        prefix = timezone.now().strftime("%Y/%m/%d")
        file_name = uuid4().hex
        extension = os.path.splitext(filename)[-1].lower() # 확장자 추출
        return "/".join(['community_image',prefix, file_name+extension])
    
    #FK
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to_func, null=True, blank=True)

    class Meta:
        db_table = 'kingbus_community_image'


class Comment(models.Model):
    comment = models.TextField()
    like_cnt = models.PositiveIntegerField(default=0) # '좋아요 수'
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    #FK
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return self.profile.nickname
    class Meta:
        db_table = 'kingbus_community_comment'


class Recomment(models.Model):
    recomment = models.TextField()
    like_cnt = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    #FK
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    # def __str__(self) -> str:
    #     return self.profile.nickname
    class Meta:
        db_table = 'kingbus_community_recomment'


"""
일대다 관계로 모델 작성 => 다대다 관계로 바꿔줄 필요 있음.
class Profile_banned_list(models.Model):
    #FK
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)
    banned_profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.banned_profile

class Scrab(models.Model):
    #FK
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)
    scraped_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.scraped_post

class Post_like(models.Model):
    #FK
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile
    
class Comment_like(models.Model):
    #FK
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile

class Recomment_like(models.Model):
    #FK
    recomment = models.ForeignKey(Recomment, on_delete=models.CASCADE)
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile

"""