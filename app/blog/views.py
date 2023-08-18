from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def blog_post_detail(request, title):
    blog_post = get_object_or_404(BlogPost, title=title)
    return render(request, 'blog/blog_post_detail.html', {'blog_post': blog_post})


def blog_post_list(request):
    blog_posts = BlogPost.objects.all()
    return render(request, 'blog/blog_post_list.html', {'blog_posts': blog_posts})
