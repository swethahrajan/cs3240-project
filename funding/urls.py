from django.urls import path
from . import views

app_name = 'funding'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_deadline, name='add_deadline'),
    path('edit/<int:id>/', views.edit_deadline, name='edit_deadline'),
    path('register/', views.organization_register, name='saf_form'),
    path('budget/', views.budget_dashboard, name='budget_dashboard'),
    path('create-event/', views.create_event, name='create_event'),
    path('budget-sheet/<int:sheet_id>/', views.view_budget_sheet, name='view_budget_sheet'),
    path('budget-sheet/<int:sheet_id>/edit/', views.edit_budget_sheet, name='edit_budget_sheet'),
    path('event/<int:event_id>/create-sheet/', views.create_budget_sheet, name='create_budget_sheet'),
    path('budget-sheet/<int:sheet_id>/add-section/', views.create_section, name='create_section'),
    path('section/<int:section_id>/add-item/', views.create_item, name='create_item'),
    path('budget-sheet/<int:sheet_id>/export-pdf/', views.export_budget_pdf, name='export_budget_pdf'),
]