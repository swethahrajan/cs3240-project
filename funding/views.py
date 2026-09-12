from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .forms import DeadlineForm, OrganizationProfileForm, OrganizationBudgetForm, EventBudgetForm, ExpenseForm
from .models import Deadline, OrganizationProfile, OrganizationBudget, EventBudget, Event, BudgetSheet, BudgetSection, BudgetItem
from core.decorators import executive_only, member_only

@login_required
def dashboard(request):
    if not OrganizationProfile.objects.filter(user=request.user).exists():
        return redirect('funding:saf_form')

    today = timezone.now().date()
    deadlines = Deadline.objects.filter(deadline_date__gte=today).order_by('deadline_date')
    reminders = []
    for d in deadlines:
        reminder_date = d.deadline_date - timedelta(days=d.reminder_days)
        if today >= reminder_date:
            reminders.append(d)

    org_profile = OrganizationProfile.objects.filter(user=request.user).first()
    org_budget = OrganizationBudget.objects.filter(organization=org_profile).first()
    events = Event.objects.filter(organization=org_profile).order_by('-date')
    sheets = BudgetSheet.objects.filter(event__in=events)

    from funding_sources.models import FundingSource
    from django.db.models import Sum
    total_funding = FundingSource.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'funding/dashboard.html', {
        'deadlines': deadlines,
        'reminders': reminders,
        'org_profile': org_profile,
        'org_budget': org_budget,
        'events': events,
        'sheets': sheets,
        'total_funding': total_funding,
    })

@executive_only
def add_deadline(request):
    if request.method == 'POST':
        form = DeadlineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('funding:dashboard')
    else:
        form = DeadlineForm()

    return render(request, 'funding/deadline_form.html', {
        'form': form
    })

@executive_only
def edit_deadline(request, pk):
    deadline = get_object_or_404(Deadline, pk=pk)

    if request.method == 'POST':
        form = DeadlineForm(request.POST, instance=deadline)
        if form.is_valid():
            form.save()
            return redirect('funding:dashboard')
    else:
        form = DeadlineForm(instance=deadline)

    return render(request, 'funding/deadline_form.html', {
         'form': form
    })

@login_required
def organization_register(request):
    try:
        profile = OrganizationProfile.objects.get(user=request.user)
        already_registered = True
    except OrganizationProfile.DoesNotExist:
        profile = None
        already_registered = False

    if request.method == 'POST':
        form = OrganizationProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        if form.is_valid():
            org = form.save(commit=False)
            org.user = request.user
            org.save()
            return redirect('funding:dashboard')
    else:
        form = OrganizationProfileForm(instance=profile)

    return render(request, 'funding/saf_form.html', {
        'form': form,
        'already_registered': already_registered
    })

@login_required
def budget_dashboard(request):
    org_budget = OrganizationBudget.objects.filter(
        organization__user=request.user
    ).first()

    events = Event.objects.filter(
        organization__user=request.user
    )

    sheets = BudgetSheet.objects.filter(
        event__in=events
    )

    return render(request, 'funding/budget_dashboard.html', {
        'org_budget': org_budget,
        'events': events,
        'sheets': sheets
    })

@login_required
def create_event(request):
    if not request.user.is_executive:
        return redirect('funding:budget_dashboard')

    if request.method == "POST":
        name = request.POST.get("name")
        date = request.POST.get("date")

        org = request.user.organizationprofile

        event = Event.objects.create(
            organization=org,
            name=name,
            date=date
        )

        # AUTO-CREATE budget sheet
        BudgetSheet.objects.create(
            event=event,
            created_by=request.user
        )

        return redirect('funding:budget_dashboard')

    return render(request, 'funding/create_event.html')

@login_required
def view_budget_sheet(request, sheet_id):
    sheet = get_object_or_404(BudgetSheet, id=sheet_id)

    return render(request, "funding/view_budget_sheet.html", {
        "sheet": sheet
    })

@executive_only
def create_budget_sheet(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        sheet = BudgetSheet.objects.create(
            event=event,
            created_by=request.user
        )
        return redirect('funding:edit_budget_sheet', sheet.id)

    return render(request, "funding/edit_budget_sheet.html", {
        "event": event
    })

@executive_only
def edit_budget_sheet(request, sheet_id):
    sheet = BudgetSheet.objects.get(id=sheet_id)

    if request.method == "POST":
        for section in sheet.sections.all():
            new_name = request.POST.get(f"section_name_{section.id}")
            if new_name:
                section.name = new_name
                section.save()
            for item in section.items.all():
                item.description = request.POST.get(f"description_{item.id}")
                item.vendor = request.POST.get(f"vendor_{item.id}")
                item.quantity = request.POST.get(f"quantity_{item.id}")
                item.unit_price = request.POST.get(f"unit_price_{item.id}")
                item.is_confirmed = f"confirmed_{item.id}" in request.POST
                item.save()

        return redirect('funding:view_budget_sheet', sheet_id=sheet.id)

    return render(request, 'funding/edit_budget_sheet.html', {
        'sheet': sheet
    })

def create_section(request, sheet_id):
    sheet = BudgetSheet.objects.get(id=sheet_id)

    section = BudgetSection.objects.create(
        sheet=sheet,
        name="New Section"
    )

    return redirect('funding:edit_budget_sheet', sheet_id=sheet.id)

def create_item(request, section_id):
    section = BudgetSection.objects.get(id=section_id)

    BudgetItem.objects.create(
        section=section,
        description="New Item",
        quantity=1,
        unit_price=0
    )

    return redirect('funding:edit_budget_sheet', sheet_id=section.sheet.id)


@login_required
def export_budget_pdf(request, sheet_id):
    sheet = get_object_or_404(BudgetSheet, id=sheet_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="{sheet.event.name}_budget.pdf"'
    )

    width, height = letter
    c = canvas.Canvas(response, pagesize=letter)
    y = height - 50

    # title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y, f"{sheet.event.name} - Budget Sheet")
    y -= 30

    for section in sheet.sections.all():
        # section heading
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, section.name)
        y -= 20

        # column headers
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "Description")
        c.drawString(200, y, "Vendor")
        c.drawString(310, y, "Qty")
        c.drawString(360, y, "Unit Price")
        c.drawString(440, y, "Total")
        c.drawString(510, y, "Confirmed")
        y -= 2
        c.line(50, y, 560, y)
        y -= 14

        # rows
        c.setFont("Helvetica", 10)
        for item in section.items.all():
            if y < 60:
                c.showPage()
                y = height - 50
                c.setFont("Helvetica", 10)

            c.drawString(50, y, str(item.description)[:25])
            c.drawString(200, y, str(item.vendor or "")[:15])
            c.drawString(310, y, str(item.quantity))
            c.drawString(360, y, f"${item.unit_price}")
            c.drawString(440, y, f"${item.total}")
            c.drawString(510, y, "Yes" if item.is_confirmed else "No")
            y -= 16

        # section total
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, f"Section Total: ${section.total_cost()}")
        y -= 30

    # grand total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, f"Grand Total: ${sheet.grand_total()}")

    c.showPage()
    c.save()
    return response
