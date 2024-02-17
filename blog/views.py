from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .models import Comment, Post, Category
from .forms import AddPostForm
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from .filters import PostFilter
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test
# Create your views here.

@transaction.atomic
def render_blog(request):
    category = Category.objects.all()
    filter = PostFilter(request.GET, queryset=Post.objects.all())
    posts = sorted(filter.qs,reverse=True, key=lambda x: x.create_at)
    paginator = Paginator(posts, 3)
    PageNumber = request.GET.get("page")
    page_obj = paginator.get_page(PageNumber)
    recent_post = sorted(posts, key=lambda x: x.create_at)[:4]

    context = {
        "recent_post": recent_post,
        "categories": category,
        "posts": page_obj,
        "filter": filter,
    }
    return render(request, "blog/blog.html", context=context)

@transaction.atomic
def render_single_blog(request, id):
    posts = Post.objects.all()
    post = get_object_or_404(posts, id=id)
    categories = Category.objects.all()
    recent_post = sorted(posts, key=lambda x: x.create_at)[:4]

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            my_form = form.save(commit=False)

            my_form.post = post
            my_form.name = request.user.username
            my_form.email = request.user.email
            my_form.user = request.user
            my_form.save()
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post_id=id)
    paginator = Paginator(comments, 6)
    PageNumber = request.GET.get("page")
    page_obj = paginator.get_page(PageNumber)
    context = {
        "post": post,
        "categories": categories,
        "recent_post": recent_post,
        "form": form,
        "comments": page_obj,
        "comments_count": comments.count(),
    }

    return render(request, "blog/single-blog.html", context=context)

@transaction.atomic
@user_passes_test(lambda x: not x.profile.is_company)
def add_blog_post(request):

    if request.method == "POST":
        form = AddPostForm(request.POST, request.FILES)  #!form  here is html  content

        if form.is_valid():
            my_form = form.save(commit=False)  #! my_form here is data from form
            my_form.created_By = request.user
            my_form.save()
            return redirect(reverse("blog:render_single_blog" ,kwargs={'id':my_form.id}))
    else:
        form = AddPostForm()

    context = {
        "form": form,
    }
    return render(request, "blog/add_blog_post.html", context=context)

@transaction.atomic
@user_passes_test(lambda x: not x.profile.is_company)
def show_user_his_posts(request):
    posts = Post.objects.all().filter(created_By=request.user)
    paginator = Paginator(posts, 2)
    PageNumber = request.GET.get("page")
    page_obj = paginator.get_page(PageNumber)
    context = {
        "posts": page_obj,
    }
    return render(request, "blog/show_user_his_posts.html", context=context)

@transaction.atomic
def delete_post(request, name):
    try:
        Post.objects.get(created_By=request.user, title=name).delete()

        return HttpResponse("post is deleted successfully", status=200)
    except Post.DoesNotExist:
        return HttpResponse("you are not allowed to delete this post", status=401)


@login_required
@transaction.atomic
def replay_comment(request, post_id, parent_comment_id):

    post = Post.objects.get(id=post_id)
    comment = Comment.objects.get(id=parent_comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            my_form = form.save(commit=False)
            my_form.post = post
            my_form.name = request.user.username
            if request.user.email:
                my_form.email = request.user.email
            my_form.user = request.user
            if "comment_id" in request.POST:
                comment_id = request.POST["comment_id"]
                comment_replay_to = Comment.objects.get(id=comment_id).user.username
                my_form.replay_to = comment_replay_to
                print(my_form.replay_to)
                print(comment_replay_to)

            my_form.parent = comment

            my_form.save()

    else:
        form = CommentForm()

    replay_comments = Comment.objects.all().filter(parent=comment)
    for replay_comment in replay_comments:
        print(replay_comment)

    context = {
        "post": post,
        "comment": comment,
        "replay_comments": replay_comments,
        
    }

    return render(request, "blog/show_replay_comment.html", context=context)




def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True

    context = {
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
    }

    return JsonResponse(context)
