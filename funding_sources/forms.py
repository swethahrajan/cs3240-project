from django import forms
from .models import ExpenseCategory, FundingSource


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name', 'description', 'expected_cost']


class FundingSourceForm(forms.ModelForm):
    class Meta:
        model = FundingSource
        fields = ['name', 'amount']
