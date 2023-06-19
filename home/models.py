from django.db import models
from django.contrib.auth.models import User
from .util import generateSlug
class blog(models.Model):
    title = models.CharField(max_length=100) 
    slug=models.CharField(max_length=1000, unique=True, blank=True, null=True)
    description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images', blank=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

    
    # overwrite the save method
    
