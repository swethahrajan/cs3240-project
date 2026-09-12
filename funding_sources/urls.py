from django.urls import path
from . import views

app_name = 'funding_sources'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_category, name='add_category'),
    path('edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('<int:cat_pk>/add-source/', views.add_funding_source, name='add_funding_source'),
    path('edit-source/<int:pk>/', views.edit_funding_source, name='edit_funding_source'),
    path('delete-source/<int:pk>/', views.delete_funding_source, name='delete_funding_source'),
]
