from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField

class Topic(models.Model):
    """
    Represents a topic for a blog post
    """

    name = models.CharField(
        max_length = 50,
        unique = True,
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        kwargs = {'slug': self.slug}
        return reverse('blog:topic-detail', kwargs=kwargs)



class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

class Post(models.Model):
    """
    Represents a blog post
    """

    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]

    title = models.CharField(
        max_length=255,
        null=False,
    )
    content = RichTextUploadingField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='blog_posts',
        null=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
        null=False,
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date and time this article was published',
    )
    slug = models.SlugField(
        null=False,
        help_text='The date and time this article was published',
        unique_for_date='published',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name = 'blog_posts',
    )
    banner = models.ImageField(
        blank=True,
        null=True,
        help_text='A banner image for the post'
    )

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.published:
            kwargs = {
                'year': self.published.year,
                'month': self.published.month,
                'day': self.published.day,
                'slug': self.slug
            }
        else:
            kwargs = {'pk': self.pk}
        
        return reverse('blog:post-detail', kwargs=kwargs)

class CommentQuerySet(models.QuerySet):
    def get_queryset(self):
        return self

class Comment(models.Model):
    APPROVED = 'approved'
    PENDING = 'pending'
    DENIED = 'post'
    APPROVED_CHOICES = [
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (DENIED, 'Denied')
    ]

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    approved = models.CharField(
        max_length=10,
        choices=APPROVED_CHOICES,
        default=APPROVED,
        help_text='Set to "Approved" to make this comment visible to users',
        null=False,
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    objects = CommentQuerySet.as_manager()

    def __str__(self):
        return f'{self.name} re: {self.post}'

    class Meta:
        ordering = ['-created']

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    submitted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted']

    def __str__(self):
        return f'{self.submitted.date()}: {self.email}'

class PhotoContest(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    photo = models.ImageField(
        blank=True,
        null=True,
        help_text='Image submitted by user'
    )
    submitted = models.DateTimeField(auto_now_add=True)
