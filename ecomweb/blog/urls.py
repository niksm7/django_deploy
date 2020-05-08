from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="BlogHome"),
    path("blogpost/<int:id>", views.blogpost, name="blogHome"),
    #API to post a comment
    path("blogpost/postComment",views.postComment,name="postComment"),
]