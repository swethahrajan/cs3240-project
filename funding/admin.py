from django.contrib import admin
from .models import Deadline

# finance officers/admin can add deadlines
admin.site.register(Deadline)
