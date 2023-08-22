from django.urls import path
from . import views


app_name = "blog"


urlpatterns = [
    # Other URL patterns
    path('blogs/', views.blog_post_list, name='blog_post_list'),
    path('blog/<str:title>/', views.blog_post_detail, name='blog_post_detail'),
]
