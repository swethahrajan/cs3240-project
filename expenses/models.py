from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank = True)

    def __str__(self):
        return self.name
    
class Expense(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    amount = models.DecimalField(max_digits = 10, decimal_places = 2)
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add = True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return self.title
    
    
class Payment(models.Model):
    expense = models.ForeignKey(Expense, on_delete = models.CASCADE)
    amount_paid = models.DecimalField(max_digits = 10, decimal_places = 2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment for {self.expense.title}"