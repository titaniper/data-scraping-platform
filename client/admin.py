from django.contrib import admin
from .models import Tag
from .models import Category
from .models import Request
from .models import RequestHistory
from .models import Pipeline
from .models import Stage
from .models import Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Request)
admin.site.register(RequestHistory)
admin.site.register(Pipeline, MarkdownxModelAdmin)
admin.site.register(Stage)
admin.site.register(Comment)
