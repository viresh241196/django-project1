from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True)
    account_number = models.IntegerField(null=True, blank=True, )
    savings = models.IntegerField(null=True, blank=True)
    date_of_birth = models.CharField(max_length=20, null=True, blank=True, default='')
    adharcard_number = models.IntegerField(null=True, blank=True, default='')
    profile_image = models.ImageField(upload_to='profile_image', default='default.jpg')
    address = models.TextField(null=True, blank=True, default="")
    mobile_number = models.IntegerField(null=True, blank=True, default='')
    email = models.EmailField(null=True, blank=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        image = Image.open(self.profile_image.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.profile_image.path)


class Passbook(models.Model):
    time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    deposit = models.IntegerField(null=True, blank=True)
    withdraw = models.IntegerField(null=True, blank=True)
    savings = models.IntegerField(null=True, blank=True)
    account_number = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
