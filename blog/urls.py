from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from . import views


urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='create_post'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='delete_post'),
    path('post/<int:pk>/comment/', views.comment, name='comment'),
    path('drafts/', views.post_drafts, name='post_drafts'),
    # path('post/new/publish/', views.publish_new_post, name='publish_new'),
    # path('post/<int:pk>/publish/', views.publish, name='publish'),
]