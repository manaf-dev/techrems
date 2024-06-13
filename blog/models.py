from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

import uuid

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slugTitle = slugify(self.title)
            unique_suffix = str(uuid.uuid4())[:4]
            self.slug = f"{slugTitle}-{unique_suffix}"
            while Post.objects.filter(slug=self.slug).exists():
                unique_suffix = str(uuid.uuid4())[:4]
                self.slug = f"{slugTitle}-{unique_suffix}"
        super().save(*args, **kwargs)
    
    def generate_unique_slug(self):
        slugTitle = slugify(self.title)
        unique_suffix = str(uuid.uuid4())[:4]
        unique_slug = f"{slugTitle}-{unique_suffix}"
        while Post.objects.filter(slug=unique_slug).exists():
            unique_suffix = str(uuid.uuid4())[:4]
            unique_slug = f"{slugTitle}-{unique_suffix}"
        return unique_slug
    

    def total_likes(self):
        return self.likes.count()

    def publish(self):
        self.published_date = timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_date']
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug':self.slug})


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.text}'