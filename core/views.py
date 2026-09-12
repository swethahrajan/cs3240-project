from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import User
from .forms import ProfileForm
from .decorators import user_admin_only
from expenses.models import Expense
from reimbursements.models import Reimbursement
from funding.models import OrganizationBudget, Deadline, Event
from django.db.models import Sum
from django.utils import timezone

def home(request):
    context = {}
    if request.user.is_authenticated:
        expenses = Expense.objects.all().order_by('-submitted_at')
        reimbursements = Reimbursement.objects.all().order_by('-submitted_at')

        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        pending_expenses = expenses.filter(status='pending').count()
        confirmed_expenses = expenses.filter(status='confirmed').count()
        total_reimbursements = reimbursements.aggregate(Sum('amount'))['amount__sum'] or 0

        today = timezone.now().date()
        upcoming_deadlines = Deadline.objects.filter(
            deadline_date__gte=today
        ).order_by('deadline_date')[:3]

        recent_expenses = expenses[:3]
        recent_reimbursements = reimbursements[:3]

        try:
            org_budget = OrganizationBudget.objects.get(
                organization__user=request.user
            )
        except OrganizationBudget.DoesNotExist:
            org_budget = None

        upcoming_events = Event.objects.filter(
            organization__user=request.user,
            date__gte=today
        ).order_by('date')[:3]

        context = {
            'total_expenses': total_expenses,
            'pending_expenses': pending_expenses,
            'confirmed_expenses': confirmed_expenses,
            'total_reimbursements': total_reimbursements,
            'upcoming_deadlines': upcoming_deadlines,
            'recent_expenses': recent_expenses,
            'recent_reimbursements': recent_reimbursements,
            'org_budget': org_budget,
            'upcoming_events': upcoming_events,
        }
    return render(request, 'core/home.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'core/profile.html', {
        'form': form
    })

@user_admin_only
def role_management(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_role = request.POST.get('role')
        
        try:
            target_user = User.objects.get(id=user_id)
            
            # Ensure we are not modifying an administrator or superuser, 
            # and we cannot assign them the User Administrator role.
            if target_user.is_superuser or target_user.is_user_admin:
                messages.error(request, "Cannot modify administrator roles.")
            elif new_role not in ['Executive', 'Member', 'None']:
                messages.error(request, "Invalid role selected.")
            else:
                target_user.groups.clear()
                if new_role != 'None':
                    group, _ = Group.objects.get_or_create(name=new_role)
                    target_user.groups.add(group)
                messages.success(request, f"Role successfully updated for {target_user.email}")
                
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            
        return redirect('role_management')

    # Get only non-administrator users
    users = User.objects.exclude(is_superuser=True).exclude(groups__name='User Administrator')
    
    # Render with all users and their current roles evaluated via properties
    return render(request, 'core/role_management.html', {
        'users': users
    })
