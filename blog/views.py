from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone

from .models import Post, Comment
from .forms import CreatePost, CreateComment

# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'blog/home.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)
    context = {'post':post, 'comments':comments}
    return render(request, 'blog/post_detail.html', context)


def create_post(request):
    form = CreatePost()
    if request.method == 'POST':
        form = CreatePost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.publication_date = timezone.now()
            post.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)


def edit_post(request, pk):
    # Get the object from database by primary key (id).
    post = get_object_or_404(Post, pk=pk)
    form = CreatePost(instance=post)
    # If this is a POST request then process the Form data.
    if request.method == "POST":
        # Create a form instance and populate it with data from the request:
        form = CreatePost(request.POST, instance=post)
        # Check whether it's valid:
        if form.is_valid():
            # Save the changes to the model using save method of our form class.
            form.save()
            return redirect('post_detail', pk=pk)
    Context = {'form':form}
    return render(request, 'blog/create_post.html', Context)


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method=='POST' :
        post.delete()
        return redirect('home')
    return render(request, 'blog/delete.html', {'post':post})


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
    
    