from django.shortcuts import render
from .models import Blogpost

def index(request):
    products = Blogpost.objects.all()
    return render(request,'blog/index.html',{'products':products})

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id=id)[0]
    products = Blogpost.objects.all()
    range1 = len(products)
    if id!=range1 and id!=1:
        post_next = Blogpost.objects.filter(post_id=id + 1)[0]
        post_prev = Blogpost.objects.filter(post_id=id - 1)[0]
        return render(request, 'blog/blogpost.html',
                      {'post': post, 'id': id, 'next_id': id + 1, 'prev_id': id - 1, 'len': range1,
                       'post_next': post_next, 'post_prev': post_prev})
    elif id==range1:
        post_prev = Blogpost.objects.filter(post_id=id - 1)[0]
        return render(request, 'blog/blogpost.html',
                      {'post': post, 'id': id, 'next_id': id + 1, 'prev_id': id - 1, 'len': range1,
                       'post_next':" ", 'post_prev': post_prev})
    elif id==1:
        post_next = Blogpost.objects.filter(post_id=id + 1)[0]
        return render(request, 'blog/blogpost.html',
                      {'post': post, 'id': id, 'next_id': id + 1, 'prev_id': id - 1, 'len': range1,
                       'post_next': post_next, 'post_prev': " "})



