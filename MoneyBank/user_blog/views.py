from django.shortcuts import render, redirect
from .models import Post
from .form import NewPostForm
from django.contrib import messages


def home(request):
    posts = Post.objects.order_by("-date")
    content = {'posts': posts}
    return render(request, 'user_blog/home.html', content)


def new_post(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            img = form.cleaned_data['image']
            content = form.cleaned_data['content']
            new = Post.objects.create(title=title, content=content, author=request.user, image=img)
            messages.success(request, f"Your new post has successfully posted.")
            return redirect('user_home')

    else:
        form = NewPostForm()
        return render(request, 'user_blog/new_post.html', {'form': form})


def detail_post(request,id):
    post = Post.objects.get(id = id)
    return render(request,'user_blog/detail_post.html',{'post':post})


def user_post(request,author_id):
    posts = Post.objects.filter(author_id=author_id).order_by("-date")
    context = {'posts':posts}
    return render(request,'user_blog/user_posts.html',context)