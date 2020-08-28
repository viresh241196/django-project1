from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_img',default='default.jpg')
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 650 or img.width > 650:
            output_size = (650,650)
            img.thumbnail(output_size)
            img.save(self.image.path)