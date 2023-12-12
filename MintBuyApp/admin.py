from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(CATEGORIES)
admin.site.register(PRODUCT)
admin.site.register(CART)
