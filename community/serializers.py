from dataclasses import field
from rest_framework import serializers
from community.models import Image, Post, Profile, Comment, Recomment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['view', 'like_cnt']
    # profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False)
    profile = serializers.CharField(required=False)
    image = serializers.ImageField(use_url=True, required=False)
    def validate(self, attrs):
        attrs['profile'] = self.context['request'].user.profile
        return attrs
    def create(self, validated_data): #https://velog.io/@han0707/Django-multiple-image
        post = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Image.objects.create(post=post, image=image_data)
        return post

class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['content', 'date_created', 'date_modified']    

class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    images = serializers.SerializerMethodField()

    def get_images(self, obj): # https://eunjin3786.tistory.com/268
        image = obj.image_set.all()
        return ImageSerializer(instance=image, many=True).data

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'



class PostCommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    recomments = serializers.SerializerMethodField()

    def get_recomments(self, obj):
        recomment = obj.recomment_set.all()
        return  RecommentSerializer(instance=recomment, many=True).data

class RecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = '__all__'



class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['like_cnt']

class PostCommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = ['like_cnt', 'post', 'profile']

class PostRecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        exclude = ['like_cnt']

class PostRecommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        exclude = ['like_cnt', 'comment', 'profile']