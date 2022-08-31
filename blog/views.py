from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from . import models, forms
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView
from django.contrib import messages
from datetime import datetime
import re
from django.contrib.auth.decorators import login_required, permission_required

class HomeView(TemplateView):
    """The Blog homepage"""
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        # Get the parent context
        context = super().get_context_data(**kwargs)
        
        # Get last 3 posts
        latest_posts = models.Post.objects.published().order_by('-published')[:3]

        # Update the context with our context variables
        context.update({
            'latest_posts': latest_posts,
        })

        return context

class AboutView(TemplateView):
    """Renders the About page view"""
    template_name = 'blog/about.html'

def PostListView(request):
    posts = models.Post.objects.published().order_by('-published')
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        post = models.Post.objects.filter(id=post_id).first()
        if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
            post.delete()

    return render(request, 'blog/post_list.html', {"posts": posts})

class PostDetailView(DetailView):
    model = models.Post

    def get_queryset(self):
        # If this is a `pk` lookup, use default queryset
        if 'pk' in self.kwargs:
            return super().get_queryset()

        # Otherwise, filter on the published date
        queryset = super().get_queryset().published()
        return queryset.filter(
            published__year=self.kwargs['year'],
            published__month=self.kwargs['month'],
            published__day=self.kwargs['day'],
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the post object
        post = self.get_object()

        # Set the post field on the form
        comment_form = forms.CommentForm(initial={'post': post})
        comments = models.Comment.objects.filter(post=post)

        context['comment_form'] = comment_form
        context['comments'] = comments.order_by('-created')

        return context

class TopicListView(ListView):
    model = models.Topic
    context_object_name = 'topics'
    queryset = models.Topic.objects.filter(blog_posts__status=models.Post.PUBLISHED).distinct().order_by('name')

class TopicDetailView(DetailView):
    model = models.Topic
    def get_queryset(self):
        return super().get_queryset().order_by('blog_posts__published')

class ContactFormView(CreateView):
    model = models.Contact
    success_url = reverse_lazy('blog:home')
    fields = [
        'first_name',
        'last_name',
        'email',
        'message',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your message has been sent.'
        )
        return super().form_valid(form)

class PhotoContestFormView(CreateView):
    model = models.PhotoContest
    success_url = reverse_lazy('blog:home')
    fields = [
        'name',
        'email',
        'photo',
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            'Thank you! Your submission has been received.'
        )
        return super().form_valid(form)

@login_required(login_url="/login/")
def create_post(request):
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = re.sub(r"[^a-zA-Z0-9 ]", "", post.title.lower()).replace(' ', '-')
            if post.status == "published":
                post.published = datetime.now()
            post.save()
            for topic in form.cleaned_data['topics']:
                post.topics.add(topic)
            post.save()
            
            return redirect("/cal/")
    else:
        form = forms.PostForm()

    return render(request, 'blog/create_post.html', {"form": form})