from django.urls import path
from . import views

urlpatterns = [
    path("", views.expense_list, name="expense_list"),
    path("approve/<int:expense_id>/", views.approve_expense, name="approve_expense"),
    path("pay/<int:expense_id>/", views.mark_paid, name="mark_paid"),
]