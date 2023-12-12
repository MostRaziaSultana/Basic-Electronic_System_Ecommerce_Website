from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class AboutUs(models.Model):
    title = models.CharField(max_length=50,null=True)
    description = RichTextField()
    image = models.ImageField(upload_to='aboutimage/',null=True)


class ContactUs(models.Model):
    title = models.CharField(max_length=500, null=True)
    address = models.CharField(max_length=200)
    mobile = models.CharField(max_length=20)
    hotline = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    support_mail = models.EmailField(max_length=30)

    def __str__(self):
        return f"{self.email}"