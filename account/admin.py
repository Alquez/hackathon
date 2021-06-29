from django.contrib import admin
from account.models import CustomUser, Profile
from django.contrib.auth.models import Group
from product.models import Product

admin.site.register(Product)
admin.site.unregister(Group)
admin.site.register(CustomUser)