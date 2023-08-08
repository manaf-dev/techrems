from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/comment/', views.comment, name='comment'),
    path('drafts/', views.post_drafts, name='post_drafts'),
    path('post/new/publish/', views.publish_new_post, name='publish_new'),
    path('post/<int:pk>/publish/', views.publish, name='publish'),
]