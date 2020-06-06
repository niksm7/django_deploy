from django.contrib import admin

# Register your models here.
from .models import Product,Contact,Orders,OrderUpdate,ShopReview,Cart
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(ShopReview)
admin.site.register(Cart)