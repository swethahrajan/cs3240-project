from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Deadline(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    deadline_date = models.DateField()
    reminder_days = models.IntegerField(default=7)

    def __str__(self):
        return self.title

class OrganizationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization_name = models.CharField(max_length=255, unique=True)

    # SAF application file (uploaded once, reused)
    saf_application = models.FileField(upload_to='saf_applications/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.organization_name}"

# Organization-wide budget (general funds)
class OrganizationBudget(models.Model):
    organization = models.OneToOneField(OrganizationProfile, on_delete=models.CASCADE)
    total_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.organization} - Organization Budget"

# Event-specific budgets
class Event(models.Model):
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.name

class EventBudget(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    allocated_funds = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.event.name} Budget"

# Spending tracking
class Expense(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE)

    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class BudgetSheet(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="Budget Spreadsheet")

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.event.name} Budget Sheet"

    def grand_total(self):
        return sum(section.total_cost() for section in self.sections.all())

class BudgetSection(models.Model):
    sheet = models.ForeignKey(BudgetSheet, on_delete=models.CASCADE, related_name="sections")
    name = models.CharField(max_length=100)  # e.g., Travel, Food, Accessories

    def __str__(self):
        return f"{self.name} ({self.sheet.event.name})"

    def total_cost(self):
        return sum(item.total for item in self.items.all())

class BudgetItem(models.Model):
    section = models.ForeignKey(BudgetSection, on_delete=models.CASCADE, related_name="items")

    description = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from decimal import Decimal

        self.quantity = int(self.quantity)
        self.unit_price = Decimal(self.unit_price)

        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description