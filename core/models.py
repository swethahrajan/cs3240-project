from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model.
    """
    @property
    def is_executive(self):
        return self.groups.filter(name='Executive').exists()

    @property
    def is_member(self):
        return self.groups.filter(name='Member').exists()

    @property
    def is_user_admin(self):
        return self.groups.filter(name='User Administrator').exists()