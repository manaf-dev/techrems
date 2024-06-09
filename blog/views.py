from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Post, Comment
from .forms import CreatePost, CreateComment

# Create your views here.
# def home(request):
#     posts = Post.objects.filter(published_date__isnull=False)
#     context = {'posts':posts}
#     return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trending_posts'] = Post.objects.order_by('-views', '-likes')[:3]
        return context
        
    

    
def postDetail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.views += 1
    post.save()
    comments = Comment.objects.filter(post=post).order_by('-date_posted')
    total_likes = post.total_likes()
    trending_posts = Post.objects.filter(author=post.author).order_by('-views', '-likes')[:3]
    context = {'post':post, 'comments':comments, 'total_likes':total_likes, 'trending_posts':trending_posts}
    return render(request, 'blog/post_detail.html', context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    
    # Set author by the login user automatically
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



@login_required
def comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(
            author=request.user,
            post=post,
            text=comment
        )
        return redirect('post_detail', post.id)
    return redirect('post_detail', post.id)
    

def likePost(request, pk):
    post = Post.objects.get(id=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return JsonResponse({'total_likes':post.total_likes(), 'liked':liked})

def post_drafts(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    context = {'posts':posts}
    return render(request, 'blog/post_drafts.html', context)

