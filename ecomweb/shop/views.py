import json
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from math import ceil
import datetime,pytz
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Product,Contact,Orders,OrderUpdate,ShopReview
from django.contrib.auth.models import User
from shop.templatetags import my_filters,convertInt,extras

def index(request):
    allProds = []
    catprod = Product.objects.values('category','id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = (n // 4) + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds':allProds}
    return render(request,'shop/index.html',params)

def searchMatch1(query,item):
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def searchMatch2(query,item):
    if len(query.split())>1:
        for i in query.split():
            if i in item.desc.lower() or i in item.product_name.lower() or i in item.category.lower():
                return True
    else:
        return False

def search(request):
    query =request.GET.get('search')
    allProds = []
    catprod = Product.objects.values('category','id')
    cats = {item['category'] for item in catprod}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch1(query.lower(),item)]
        if len(prod)<2:
            prod = prod + [item for item in prodtemp if searchMatch2(query.lower(), item)]
        n = len(prod)
        nSlides = (n // 4) + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod,range(1,nSlides),nSlides])
    params = {'allProds':allProds,'msg':"",'query':query}
    if len(allProds)==0 or len(query)<2:
        params = {'msg': "Please enter relevant query!"}
    return render(request,'shop/search.html',params)


def about(request):
    return render(request,'shop/about.html')

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thank = True
        return render(request, 'shop/contact.html',{'thank':thank})
    return render(request, 'shop/contact.html')

def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId','')
        email = request.POST.get('email','')
        try:
            order = Orders.objects.filter(order_id = orderId,email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'date':item.timestamp,"time":item.timestamp1})
                    response = json.dumps({"status":"success","updates":updates,"itemsJson":order[0].items_json},default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception:
            return HttpResponse('{"status":"error"}')
    return render(request, 'shop/tracker.html')

def productview(request,myid):
    #Fetch the product using id
    product = Product.objects.filter(id=myid)[0]
    reviews = ShopReview.objects.filter(product=product,parent=None)
    replies = ShopReview.objects.filter(product=product).exclude(parent=None)
    repDict = {}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    product_all = Product.objects.all()
    return render(request, 'shop/prodView.html',{'product':product,'product_all':product_all,'reviews':reviews,'replyDict':repDict})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson','')
        name = request.POST.get('firstName','')+" "+request.POST.get('lastName','')
        amount = request.POST.get('amount','')
        email = request.POST.get('email','')
        address = request.POST.get('address1','')+" "+request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        order = Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        thank = True
        now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        timex = now.strftime("%H:%M:%S")
        update = OrderUpdate(order_id=order.order_id,update_desc="The order has been placed",timestamp1=timex)
        update.save()
        id = order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank,'id':id})
    return render(request, 'shop/checkout.html')

def cart(request):
    return render(request,'shop/cart.html')

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

def postReview(request):
    if request.method == "POST":
        review = request.POST.get("review")
        user = request.user
        productSno = request.POST.get("productSno")
        product = Product.objects.filter(id=productSno)[0]
        parentSno = request.POST.get("parentSno")
        rating = request.POST.get("rating-value")
        if parentSno=="":
            review = ShopReview(review=review,user=user,product=product,rating=rating)
            review.save()
            messages.success(request,"Your comment has been posted successfully!")
        else:
            parent = ShopReview.objects.filter(sno=parentSno)[0]
            comment = ShopReview(review=review,user=user,product=product,parent=parent)
            comment.save()
            messages.success(request,"Your Reply has been posted successfully!")

        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))

    else:
        return HttpResponse('404 - Error Found')