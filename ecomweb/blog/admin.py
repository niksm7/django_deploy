from django.contrib import admin
from .models import Blogpost,BlogComment
# Register your models here.
admin.site.register((Blogpost,BlogComment))