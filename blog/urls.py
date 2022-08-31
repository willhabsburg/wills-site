# blog/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from . import views

# Namespace for the API app
app_name = 'blog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('posts/', views.PostListView, name='post-list'),
    path(
        'posts/<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.PostDetailView.as_view(),
        name='post-detail',
    ),
    path(
        'posts/<int:pk>/',
        views.PostDetailView.as_view(),
        name='post-detail'
    ),
    path('topics/', views.TopicListView.as_view(), name='topic-list'),
    path(
        'topics/<slug:slug>/',
        views.TopicDetailView.as_view(),
        name='topic-detail'
    ),
    path(
        'contact/',
        login_required(login_url='/login/')(views.ContactFormView.as_view()),
        name='contact'
    ),
    path(
        'photocontest/',
        login_required(login_url='/login/')(views.PhotoContestFormView.as_view()),
        name='photocontest'
    ),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('create_post/', views.create_post, name='create_post'),
]