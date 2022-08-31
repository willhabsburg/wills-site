# blog/context_processors.py

from django.db.models import Count
from . import models

def base_context(request):
        all_topics =  models.Topic.objects.filter(blog_posts__status=models.Post.PUBLISHED).annotate(Count('blog_posts')) \
            .order_by('-blog_posts__count')[:10]

        return {'all_topics': all_topics}