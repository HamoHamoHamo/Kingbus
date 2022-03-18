from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.settings import api_settings
# from rest_framework.pagination import PageNumberPagination

from .serializers import PostCommentDetailSerializer, PostCommentListSerializer, PostCommentSerializer, PostDetailSerializer, PostListSerializer, PostRecommentDetailSerializer, PostRecommentSerializer, PostSerializer
from .models import Comment, Post, Recomment

def invalid_credentials():
    return Response({"message": "Invalid Credentials"}, status=status.HTTP_403_FORBIDDEN)

    
class PostView(APIView):
    def post(self, request):
        # requestdata = request.data.copy()
        # print(request.user.profile)
        # requestdata['profile'] = request.user.profile
        serializer = PostSerializer(data=request.data, context={'request':request})
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'detail': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


class PostListView(ListAPIView): #https://ssungkang.tistory.com/entry/Django-DRF-Pagination
    queryset = Post.objects.order_by('-pk')
    serializer_class = PostListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS


class PostDetailView(APIView):
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs['board_id'])
        return Response(self.serializer_class(post).data)


    def put(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs['board_id'])
        if post.profile != request.user.profile:
            return invalid_credentials()
        serializer = self.serializer_class(instance=post, data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'detail': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


    def delete(self, request, **kwargs):
        post = get_object_or_404(Post, id=kwargs['board_id'])
        if post.profile == request.user.profile:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return invalid_credentials()


class PostCommentView(APIView):
    def post(self, request, **kwargs):
        if kwargs:
            return Response({"detail": "Method \"POST\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'detail': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


    def patch(self, request, **kwargs):
        if not 'comment_id' in kwargs:
            return Response({"detail": "Method \"PATCH\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        serializer = PostCommentDetailSerializer(instance=comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'detail': PostCommentDetailSerializer(comment).data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, **kwargs):
        if not 'comment_id' in kwargs:
            return Response({"detail": "Method \"DELETE\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        comment = get_object_or_404(Comment, id=kwargs['comment_id'])
        print(comment.profile, request.user.profile)
        if comment.profile == request.user.profile:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return invalid_credentials()


class PostRecommentView(APIView):
    def post(self, request, **kwargs):
        if kwargs:
            return Response({"detail": "Method \"POST\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        serializer = PostRecommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'detail': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


    def patch(self, request, **kwargs):
        if not 'recomment_id' in kwargs:
            return Response({"detail": "Method \"PATCH\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        recomment = get_object_or_404(Recomment, id=kwargs['recomment_id'])
        serializer = PostRecommentDetailSerializer(instance=recomment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'detail': PostRecommentDetailSerializer(recomment).data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    def delete(self, request, **kwargs):
        if not 'recomment_id' in kwargs:
            return Response({"detail": "Method \"DELETE\" not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        recomment = get_object_or_404(Recomment, id=kwargs['recomment_id'])
        print(recomment.profile, request.user.profile)
        if recomment.profile == request.user.profile:
            recomment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return invalid_credentials()


class PostCommentListView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, **kwargs):
        # if 'board_id' in kwargs:
        comment = Comment.objects.filter(post__id=kwargs['board_id'])
        #recomment = Recomment.objects.filter(comment__in=comment) #https://dev-jacob.tistory.com/entry/Django-QuerySet-Value-%EC%97%90%EB%9F%AC-%ED%95%B4%EA%B2%B0%ED%95%98%EA%B8%B0
        response = {
            'comment': PostCommentListSerializer(comment, many=True).data
        }
        return Response(response, status=status.HTTP_200_OK)
