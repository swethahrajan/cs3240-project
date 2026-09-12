from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.decorators import executive_only
from .models import Expense


@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, "expenses/expense_list.html", {"expenses": expenses})


@login_required
@executive_only
def approve_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.status = 'confirmed'
    expense.save()
    return redirect('expense_list')


@login_required
@executive_only
def mark_paid(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    expense.status = 'paid'
    expense.save()
    return redirect('expense_list')
