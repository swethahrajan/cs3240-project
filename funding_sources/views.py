from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
# from core.decorators import executive_only
from .models import ExpenseCategory, FundingSource
from .forms import ExpenseCategoryForm, FundingSourceForm


@login_required
def dashboard(request):
    categories = ExpenseCategory.objects.prefetch_related('funding_sources').all()
    category_data = []
    for cat in categories:
        total_received = sum(fs.amount for fs in cat.funding_sources.all())
        category_data.append({
            'category': cat,
            'funding_sources': cat.funding_sources.all(),
            'total_received': total_received,
        })
    return render(request, 'funding_sources/dashboard.html', {
        'category_data': category_data,
    })


@login_required
def add_category(request):
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funding_sources:dashboard')
    else:
        form = ExpenseCategoryForm()
    return render(request, 'funding_sources/category_form.html', {'form': form})


@login_required
def edit_category(request, pk):
    category = get_object_or_404(ExpenseCategory, pk=pk)
    if request.method == 'POST':
        form = ExpenseCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('funding_sources:dashboard')
    else:
        form = ExpenseCategoryForm(instance=category)
    return render(request, 'funding_sources/category_form.html', {'form': form})


@login_required
def delete_category(request, pk):
    if request.method != 'POST':
        return redirect('funding_sources:dashboard')
    category = get_object_or_404(ExpenseCategory, pk=pk)
    category.delete()
    return redirect('funding_sources:dashboard')


@login_required
def add_funding_source(request, cat_pk):
    category = get_object_or_404(ExpenseCategory, pk=cat_pk)
    if request.method == 'POST':
        form = FundingSourceForm(request.POST)
        if form.is_valid():
            source = form.save(commit=False)
            source.category = category
            source.save()
            return redirect('funding_sources:dashboard')
    else:
        form = FundingSourceForm()
    return render(request, 'funding_sources/funding_source_form.html', {
        'form': form,
        'category': category,
    })


@login_required
def edit_funding_source(request, pk):
    source = get_object_or_404(FundingSource, pk=pk)
    if request.method == 'POST':
        form = FundingSourceForm(request.POST, instance=source)
        if form.is_valid():
            form.save()
            return redirect('funding_sources:dashboard')
    else:
        form = FundingSourceForm(instance=source)
    return render(request, 'funding_sources/funding_source_form.html', {
        'form': form,
        'category': source.category,
    })


@login_required
def delete_funding_source(request, pk):
    if request.method != 'POST':
        return redirect('funding_sources:dashboard')
    source = get_object_or_404(FundingSource, pk=pk)
    source.delete()
    return redirect('funding_sources:dashboard')
