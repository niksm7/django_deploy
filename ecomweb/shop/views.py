import json
from math import ceil
import datetime,pytz
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product,Contact,Orders,OrderUpdate

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
    product = Product.objects.filter(id=myid)
    print(type(product[0].id))
    product_all = Product.objects.all()
    return render(request, 'shop/prodView.html',{'product':product[0],'product_all':product_all})


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
