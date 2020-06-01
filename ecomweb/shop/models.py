from django.db import models
import datetime,pytz
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
import django.utils.timezone as dut

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.product_name

class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=70,default="")
    email = models.CharField(max_length=70,default="")
    desc = models.TextField(max_length=500,default="")

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111,default="")

    def __str__(self):
        return self.name+"(id:"+str(self.order_id)+")"

now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
timex= now.strftime("%H:%M:%S")

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(_("Date"),default=datetime.date.today)
    timestamp1 = models.TimeField(_("Time"),default="")

    def __str__(self):
        return self.update_desc[0:17]+"..."

class ShopReview(models.Model):
    sno = models.AutoField(primary_key = True)
    review = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timestamp = models.DateTimeField(default=dut.now)
    rating = models.IntegerField(default=1)

    def __str__(self):
        return self.review[0:13]+"... "+"by "+self.user.username