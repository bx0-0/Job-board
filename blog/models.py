import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)
    id = uuid4()
    return f"PostsImages/{id}{ext}"

class Post(models.Model):
    created_By = models.ForeignKey(User, related_name='post',on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    post_content = models.TextField()
    post_image = models.ImageField(upload_to=GetImageUploadTo)
    create_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category' , related_name="post_category",on_delete=models.SET_NULL,null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    
    def total_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=25, default="")

    def __str__(self) -> str:
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField()
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', related_name='replay',blank=True, null=True,on_delete =models.CASCADE)
    replay_to = models.CharField(max_length=30, blank=True,null=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment by {}'.format(self.name)
    
    