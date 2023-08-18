from django.contrib import admin

# Register your models here.
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'content',
        'publish_date',
        'meta_description',
        'keywords',
        'image',
    )
    list_filter = ('publish_date',)