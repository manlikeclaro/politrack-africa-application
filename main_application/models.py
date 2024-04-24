from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Report(models.Model):
    report_name = models.CharField(max_length=256)
    report_file = models.FileField(upload_to='reports', null=True)
    release_date = models.DateField()
    slug = models.SlugField(default='')
    created_on = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.report_name)
        super().save()

    def __str__(self):
        return f'{self.report_name}'


class Blog(models.Model):
    title = models.CharField(max_length=200)
    # content = models.TextField()
    content = CKEditor5Field(config_name='extends', null=True, default='')
    image = CloudinaryField('image', null=True)
    slug = models.SlugField(default='', unique=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save()

    def __str__(self):
        return self.title


class CustomerMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.TextField()
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name_plural = "Customer Messages"
