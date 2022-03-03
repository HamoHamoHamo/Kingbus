from dataclasses import field
from rest_framework import serializers
from community.models import Image, Post


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['view', 'like_cnt']
    image = serializers.ImageField(use_url=True)


    def validate(self, attrs):
        print(attrs['profile'])
        print(self.context['request'].user.profile)
        attrs['profile'] = self.context['request'].user.profile
        return attrs
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            Image.objects.create(post=post, image=image_data)
        return post

    
class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        image = obj.image_set.all()
        return ImageSerializer(instance=image, many=True).data