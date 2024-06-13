from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from blog.models import Post
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'users/registration.html', context)

# @login_required()
def viewProfile(request, username):
    if not request.user.is_authenticated:
        messages.info(request, f'Login or Sign up to see the profile of {username}.')
        return redirect('/login/?next=%s' % request.path)
    recent_posts = Post.objects.order_by('-created_date')[:3]
    user_obj = User.objects.get(username=username)
    context = {'user_obj':user_obj, 'recent_posts':recent_posts}
    return render(request, 'users/view_profile.html', context)


# @login_required
def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, f'Login or Sign up to see your profile.')
        return redirect('/login/?next=%s' % request.path)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('view-profile', request.user.username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)