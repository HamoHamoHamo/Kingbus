from enum import unique
from tabnanny import verbose
from django.db import models
from user.models import User,DriverAcc,CompanyAcc

# Create your models here.

class Community_profile(models.Model):
    nickname = models.CharField(max_length=32,unique=True)
    #FK
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.nickname


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    view = models.IntegerField()
    like_cnt = models.PositiveIntegerField(default=0) # '좋아요 수'
    kinds = models.CharField(max_length=50)
    #date 관련해서 재질문하고 다시 짜기
    dt_created = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="Date Modified",auto_now=True)
    #FK
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title



class Photo(models.Model):
    photo = models.ImageField(upload_to="")
    #FK
    post = models.ForeignKey(Post,on_delete=models.CASCADE)



class Comment(models.Model):
    comment = models.TextField()
    like_cnt = models.PositiveIntegerField(default=0) # '좋아요 수'
    #date 관련해서 재질문하고 다시 짜기
    dt_created = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="Date Modified",auto_now=True)
    #FK
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    # 커뮤니티 프로필 닉네임 불러올 수 있는지
    def __str__(self) -> str:
        return self.profile.nickname


class Recomment(models.Model):
    recomment = models.TextField()
    like_cnt = models.IntegerField()
    dt_created = models.DateTimeField(verbose_name="Date Created",auto_now_add=True)
    dt_modified = models.DateTimeField(verbose_name="Date Modified",auto_now=True)
    #FK
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    profile = models.ForeignKey(Community_profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.profile.nickname



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