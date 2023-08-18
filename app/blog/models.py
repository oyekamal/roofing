from django.db import models


class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    meta_description = models.TextField(null=True, blank=True)
    keywords = models.TextField(max_length=255)
    # Add this field for the image
    image = models.ImageField(upload_to='blog_images/')
    # Add other fields as needed

    def __str__(self):
        return self.title
