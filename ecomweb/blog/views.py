from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from .models import Blogpost,BlogComment
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.templatetags import extras

def index(request):
    products = Blogpost.objects.all()
    return render(request,'blog/index.html',{'products':products})

def blogpost(request,id):
    post = Blogpost.objects.filter(post_id=id)[0]
    comments = BlogComment.objects.filter(post=post,parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    products = Blogpost.objects.all()
    range1 = len(products)
    if id!=range1 and id!=1:
        post_next = Blogpost.objects.filter(post_id=id + 1)[0]
        post_prev = Blogpost.objects.filter(post_id=id - 1)[0]
        return render(request, 'blog/blogpost.html',
                      {'post': post, 'id': id, 'next_id': id + 1, 'prev_id': id - 1, 'len': range1,
                       'post_next': post_next, 'post_prev': post_prev,'comments':comments,'user':request.user,'replyDict':repDict})
    elif id==range1:
        post_prev = Blogpost.objects.filter(post_id=id - 1)[0]
        return render(request, 'blog/blogpost.html',
                      {'post': post, 'id': id, 'next_id': id + 1, 'prev_id': id - 1, 'len': range1,
                       'post_next':" ", 'post_prev': post_prev,'comments':comments,'replyDict':repDict})
    elif id==1:
        post_next = Blogpost.objects.filter(post_id=id + 1)[0]
        return render(request, 'blog/blogpost.html',
                      {'post': post, 'id': id, 'next_id': id + 1, 'prev_id': id - 1, 'len': range1,
                       'post_next': post_next, 'post_prev': " ",'comments':comments,'replyDict':repDict})

def handleSignup(request):
    if request.method == "POST":
        #get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        emailSignup = request.POST['emailSignup']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #check for errorneous inputs
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already taken please choose some other username')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        if len(username)>10:
            messages.error(request, 'Username must be under 10 characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if not username.isalnum():
            messages.error(request,'Username must only contain alpha numeric characters')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


        #Create the user
        myuser = User.objects.create_user(username,emailSignup,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,'Your account has been successfully created')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        return HttpResponse("404 - NOT FOUND")

def handleLogin(request):
    if request.method == "POST":
        #get the post parameters
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']
        user = authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request,user)
            messages.success(request,'Successfully Logged In')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
        else:
            messages.error(request,'Invalid credentials, Please try again')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    return HttpResponse('404 - Error Found')

def handleLogout(request):
    logout(request)
    messages.success(request,'Successfully logged out')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Blogpost.objects.filter(post_id=postSno)[0]
        parentSno = request.POST.get("parentSno")

        if parentSno=="":
            comment = BlogComment(comment=comment,user=user,post=post)
            comment.save()
            messages.success(request,"Your comment has been posted successfully!")
        else:
            parent = BlogComment.objects.filter(sno=parentSno)[0]
            comment = BlogComment(comment=comment,user=user,post=post,parent=parent)
            comment.save()
            messages.success(request,"Your Reply has been posted successfully!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        return HttpResponse('404 - Error Found')

