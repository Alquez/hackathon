from django.contrib import admin

from .models import ProfileProducer, ProfileCustomer

admin.site.register(ProfileProducer)
admin.site.register(ProfileCustomer)
