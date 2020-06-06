from django.contrib import admin
from .models import Blogpost,BlogComment
# Register your models here.
admin.site.register(BlogComment)

@admin.register(Blogpost)
class BlogpostAdmin(admin.ModelAdmin):
    class Media:
        js = ('blog/tinyInject.js',)