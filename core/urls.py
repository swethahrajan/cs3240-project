from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("profile/", views.profile_view, name="profile"),
    path("roles/", views.role_management, name="role_management"),
]
