from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from main.forms import UpdateUserForm
from posts.models import Post


def index(request):
    if request.user is not None and request.user.is_authenticated:
        page_name = f"Main page | {request.user.username}"
    else:
        page_name = "Main page"

    post = post = Post.objects.latest('id')

    context={
        'page_name' : page_name,
        'post': post,
    }
    return render(request, 'main/index.html', context)


def faq(request):
    if request.user is not None and request.user.is_authenticated:
        page_name = f"FAQ page | {request.user.username}"
    else:
        page_name = "FAQ page"

    context={
        'page_name' : page_name
    }
    return render(request, 'main/faq.html', context)


@login_required
def profile(request):
    predictions = Post.objects.filter(user_id=request.user.id).order_by('-timestamp')
    context = {
        'page_name': f"Profile | {request.user.username}",
        'predictions': predictions,
    }

    return render(request, 'main/profile.html', context)


@login_required
def update_profile(request):
    user = User.objects.get(id=request.user.id)
    form = UpdateUserForm(request.POST or None, instance=user)

    context = {
        'page_name': f"Update Profile | {request.user.username}",
        'form': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            login(request, user)
            messages.success(request, 'User data has been updated.')
            return redirect('profile')
        else:
            messages.warning(request, 'Something went wrong.')
            return render(request, 'main/update_profile.html', context)

    return render(request, 'main/update_profile.html', context)


def login_page(request):
    context={
        'page_name' : 'Login page'
    }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '✅ Successful login!')
            return redirect('index')
        else:
            messages.success(request, '❌ Invalid login details!')
            return redirect('login_page')
    else:
        return render(request, 'main/login_page.html', context)


def logout_page(request):
    logout(request)
    return redirect('index')


def register_page(request):
    context = {
        'page_name': 'Register page',
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')


        if password != password_confirm:
            messages.error(request, '❌ Passwords do not match!')
            return redirect('register_page')


        if User.objects.filter(username=username).exists():
            messages.error(request, '❌ Username already exists!')
            return redirect('register_page')

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()

            login(request, user)
            messages.success(request, '✅ Registration successful! Welcome to the platform.')
            return redirect('index')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
            return redirect('register_page')

    return render(request, 'main/register_page.html', context)
