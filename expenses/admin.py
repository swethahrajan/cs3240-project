from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Vendor, Expense, Payment

admin.site.register(Vendor)
admin.site.register(Expense)
admin.site.register(Payment)