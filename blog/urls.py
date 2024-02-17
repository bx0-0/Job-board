from django.urls import path 
from . import views

app_name ="blog"

urlpatterns = [
    path('', views.render_blog ,name=''),
    path('single-blog/', views.render_single_blog ,name='single_blog'),
    path('add-blog-post/', views.add_blog_post ,name='add-blog-post'),
    path('my-posts/', views.show_user_his_posts ,name='show_user_his_posts'),
    path('delete-my-post-<str:name>/', views.delete_post ,name='delete_post'),
    path('show-post-<int:id>/', views.render_single_blog ,name='render_single_blog'),
    path('<int:post_id>/reply-<int:parent_comment_id>/', views.replay_comment ,name='replay_comment'),
    path('like-or-unlike/<int:id>', views.like_post ,name='like_post'),

   
]