from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import Group

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login with default group 'Member'. 
        """
        # Call the parent save_user to create the user object
        user = super().save_user(request, sociallogin, form)
        
        # Assign the 'Member' group (migration should have already created this)
        member_group = Group.objects.get(name='Member')
        user.groups.add(member_group)
        
        return user