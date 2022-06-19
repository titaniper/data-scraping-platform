import os.path
from turtle import mode

from django.contrib.auth.models import User
from django.db import models

from . import enums

# Create your models here.
from markdown import markdown
from markdownx.models import MarkdownxField

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/tag/{self.slug}'

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'categories'

class Request(models.Model):
    name = models.CharField(max_length=30)
    description = MarkdownxField()
    url = models.TextField(blank=False)
    method = models.TextField(blank=False)
    header = models.TextField(blank=True)
    queryParameters = models.TextField(blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]  [{self.name}] :: {self.url}'

    def get_absolute_url(self):
        return f'/requests/{self.pk}/'

    def get_markdown_description(self):
        return markdown(self.description)

class RequestHistory(models.Model):
    name = models.CharField(max_length=30)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    status = models.TextField(blank=False)
    result = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]  [{self.name}]'

    def get_absolute_url(self):
        return f'/request-histories/{self.pk}/'

    class Meta:
        verbose_name_plural = 'request-histories'

class Pipeline(models.Model):
    title = models.CharField(max_length=30)
    description = MarkdownxField()
    hook_msg = models.TextField(blank=True)
    head_image = models.ImageField(upload_to='client/images/%Y/%m/%d/', blank=True)
    attached_file = models.FileField(upload_to='client/files/%Y/%m/%d/', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True)

    aggregated_status = models.CharField(max_length=255, choices=enums.AggregatedStatus.choices())
    pipe_line_status = models.CharField(max_length=255, choices=enums.PipelineStatus.choices())

    last_success_at = models.DateTimeField(null=True, blank=True)
    last_failure_at = models.DateTimeField(null=True, blank=True)
    last_duration = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]  [{self.title}] :: {self.author}'

    def get_absolute_url(self):
        return f'/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.attached_file.name)

    def get_markdown_description(self):
        return markdown(self.description)

    class Meta:
        verbose_name_plural = 'pipelines'

class Stage(models.Model):
    title = models.CharField(max_length=30)
    description = MarkdownxField()
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    request = models.ManyToManyField(Request, blank=True)
    status = models.CharField(max_length=255, choices=enums.AggregatedStatus.choices())
    pipe_line_status = models.CharField(max_length=255, choices=enums.PipelineStatus.choices())
    last_success_at = models.DateTimeField(null=True, blank=True)
    last_failure_at = models.DateTimeField(null=True, blank=True)
    last_duration = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]  [{self.title}]'

    def get_markdown_description(self):
        return markdown(self.description)

class Comment(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} - {self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}'