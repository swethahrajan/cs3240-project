from django.contrib import admin
from .models import ExpenseCategory, FundingSource

admin.site.register(ExpenseCategory)
admin.site.register(FundingSource)
