from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import PostDetailSerializer, PostSerializer
from .models import Post

# Create your views here.



class PostView(APIView):
    serializer_class = PostSerializer

    def post(self, request):
        # requestdata = request.data.copy()
        # print(request.user.profile)
        # requestdata['profile'] = request.user.profile
        serializer = self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response = {
                'success': True,
                'statusCode': status.HTTP_201_CREATED,
                'dispatch': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)


class PostDetailView(APIView):
    serializer_class = PostDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['board_id'])
        except:
            return Response({"message": "Page Not Found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(post).data)