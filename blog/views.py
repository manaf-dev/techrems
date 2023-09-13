from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Post, Comment
from .forms import CreatePost, CreateComment

# Create your views here.
# def home(request):
#     posts = Post.objects.filter(published_date__isnull=False)
#     context = {'posts':posts}
#     return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = Comment.objects.filter(post=post)
#     context = {'post':post, 'comments':comments}
#     return render(request, 'blog/post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



# def create_post(request):
#     form = CreatePost()
#     if request.method == 'POST':
#         form = CreatePost(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('blog-home')
#     context = {'form': form}
#     return render(request, 'blog/create_post.html', context)

# def publish_new_post(request):
#     #form = CreatePost()
#     #if request.method == 'POST':
#     form = CreatePost(request.POST)
#     if form.is_valid():
#         post = form.save(commit=False)
#         post.author = request.user
#         post.save()
#         post.publish()
#         return redirect('blog-home')
#     #context = {'form': form}
#     return render(request, 'blog/home.html')

# def publish(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.publish()
#     return redirect('blog-home')

# def edit_post(request, pk):
#     # Get the object from database by primary key (id).
#     post = get_object_or_404(Post, pk=pk)
#     form = CreatePost(instance=post)
#     # If this is a POST request then process the Form data.
#     if request.method == "POST":
#         # Create a form instance and populate it with data from the request:
#         form = CreatePost(request.POST, instance=post)
#         # Check whether it's valid:
#         if form.is_valid():
#             # Save the changes to the model using save method of our form class.
#             form.save()
#             return redirect('post_detail', pk=pk)
#     Context = {'form':form, 'post':post}
#     return render(request, 'blog/create_post.html', Context)


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



# def delete_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method=='POST' :
#         post.delete()
#         return redirect('blog-home')
#     return render(request, 'blog/delete.html', {'post':post})


# class Comment(ListView):
#     model = Comment

def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    form = CreateComment()
    if request.method == 'POST':
        form = CreateComment(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('post_detail', pk=post.pk)

    context = {'post':post, 'form':form, 'comments':comments}
    return render(request, 'blog/comment.html', context)
    


def post_drafts(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    context = {'posts':posts}
    return render(request, 'blog/post_drafts.html', context)

