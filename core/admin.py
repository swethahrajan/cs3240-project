from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your custom user model with the admin site
# We use the standard UserAdmin but with our custom User model
admin.site.register(User, UserAdmin)
