from django.shortcuts import redirect, render

from .forms import ReimbursementForm
from .models import Reimbursement


def dashboard(request):
    if request.method == "POST":
        form = ReimbursementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("reimbursements:dashboard")
    else:
        form = ReimbursementForm()

    reimbursements = Reimbursement.objects.order_by("-submitted_at")
    return render(
        request,
        "reimbursements/dashboard.html",
        {"form": form, "reimbursements": reimbursements},
    )
