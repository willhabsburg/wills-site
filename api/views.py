# api/views.py

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from blog.models import Post, Comment
from . import serializers
from django.db.models import F
from django.shortcuts import render

@api_view(['GET'])
def index(request):
    return Response()

class PostListView(generics.ListAPIView):
    """
    Returns a list of published posts
    """
    serializer_class = serializers.PostListSerializer
    queryset = Post.objects.published()

class PostDetailView(generics.RetrieveAPIView):
    """
    Returns post details
    """
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.published()

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()

    def get_queryset(self):
        post_id = self.request.query_params.get('post')
        queryset = super().get_queryset()
        if post_id and post_id.isdecimal():
            queryset = queryset.filter(post_id=int(post_id))
        return queryset.order_by('-created')

    def post(self, request):
        print(request.user.email)
        print(request.POST)
        current_user = request.user
        post = Post.objects.filter(id=request.POST['post']).first()
        comment = Comment()
        comment.post = post
        comment.name = current_user.username
        comment.email = current_user.email
        comment.text = request.POST['text']
        comment.save()
        return HttpResponse('success')

def CommentLikeView(request, pk):
    queryset = Comment.objects.get(pk=pk)
    queryset.likes = F('likes') + 1
    queryset.save()
    return HttpResponse('Your upvote has been registered!')

def CommentDislikeView(request, pk):
    queryset = Comment.objects.get(pk=pk)
    queryset.dislikes = F('dislikes') + 1
    queryset.save()
    return HttpResponse('Your downvote has been registered!')
