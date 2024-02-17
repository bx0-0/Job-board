from django import forms
from .models import Post,Comment
from django.db import transaction


@transaction.atomic
class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'post_content', 'post_image', ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']        