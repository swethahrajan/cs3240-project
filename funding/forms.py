from django import forms
from .models import Deadline, OrganizationProfile, OrganizationBudget, EventBudget, Expense, BudgetSection, BudgetItem

class DeadlineForm(forms.ModelForm):
    class Meta:
        model = Deadline
        fields = ['title', 'deadline_date', 'reminder_days']

class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationProfile
        fields = ['organization_name', 'saf_application']

class OrganizationBudgetForm(forms.ModelForm):
    class Meta:
        model = OrganizationBudget
        fields = ['total_funds']

class EventBudgetForm(forms.ModelForm):
    class Meta:
        model = EventBudget
        fields = ['allocated_funds']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['event', 'description', 'amount']

class BudgetSectionForm(forms.ModelForm):
    class Meta:
        model = BudgetSection
        fields = ['name']

class BudgetItemForm(forms.ModelForm):
    class Meta:
        model = BudgetItem
        fields = ['description', 'vendor', 'quantity', 'unit_price', 'is_confirmed']